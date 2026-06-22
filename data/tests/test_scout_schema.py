#!/usr/bin/env python3
"""
测试 Scout 来源注册 schema 的可执行契约

验证：
1. Schema 能解析且结构正确
2. required 包含 resource_approval_id 和 required_scopes
3. source item 禁止 additionalProperties
4. 示例能通过验证
5. 无效 fixture（缺审批 ID、缺 scope、未知字段）失败
6. 文档不再声称具体来源必须写入 rules/
"""

import json
import os
import sys
from pathlib import Path

# 测试是否有 jsonschema，如果有则做完整验证
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def test_dependencies():
    """检查测试依赖"""
    if not HAS_YAML:
        print("FAIL: PyYAML 缺失，无法执行 schema 验证")
        return False
    if not HAS_JSONSCHEMA:
        print("FAIL: jsonschema 缺失，无法执行完整 schema 验证")
        return False
    return True


def load_schema():
    """加载 Scout source registry schema"""
    schema_path = Path(__file__).parent.parent / "exploration" / "scout-source-registry.schema.yaml"

    if not schema_path.exists():
        print(f"FAIL: Schema file not found at {schema_path}")
        return None

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = yaml.safe_load(f)

    return schema


def test_schema_structure():
    """测试 schema 基本结构"""
    schema = load_schema()
    if not schema:
        return False

    # 验证 schema 声明与 $defs 一致
    schema_version = schema.get('$schema', '')
    if '$defs' in schema:
        if 'draft-07' in schema_version:
            print("FAIL: Schema 使用 $defs 但声明 draft-07（应使用 draft/2020-12 或改用 definitions）")
            return False

    # 验证 schema 本身有效
    if HAS_JSONSCHEMA:
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except jsonschema.SchemaError as e:
            print(f"FAIL: Schema 本身无效: {e.message}")
            return False

    # 验证 schema 有顶层 sources 数组定义
    if 'properties' not in schema or 'sources' not in schema['properties']:
        print("FAIL: Schema 缺少 properties.sources 定义")
        return False

    # 验证 sources 指向 $defs/source
    sources_def = schema['properties']['sources']
    if 'items' not in sources_def or '$ref' not in sources_def['items']:
        print("FAIL: properties.sources 未正确引用 $defs/source")
        return False

    # 验证 $defs/source 存在
    if '$defs' not in schema or 'source' not in schema['$defs']:
        print("FAIL: Schema 缺少 $defs/source 定义")
        return False

    print("PASS: Schema 结构正确（顶层 sources 数组，source item 在 $defs）")
    return True


def test_required_fields():
    """测试 source item 的 required 字段"""
    schema = load_schema()
    if not schema:
        return False

    source_def = schema['$defs']['source']
    required = source_def.get('required', [])

    # 验证 resource_approval_id 是 required
    if 'resource_approval_id' not in required:
        print("FAIL: source.required 缺少 resource_approval_id")
        return False

    # 验证 required_scopes 是 required
    if 'required_scopes' not in required:
        print("FAIL: source.required 缺少 required_scopes")
        return False

    print("PASS: source.required 包含 resource_approval_id 和 required_scopes")
    return True


def test_additional_properties():
    """测试 source item 禁止 additionalProperties"""
    schema = load_schema()
    if not schema:
        return False

    source_def = schema['$defs']['source']

    if source_def.get('additionalProperties') is not False:
        print("FAIL: source item 未设置 additionalProperties: false")
        return False

    print("PASS: source item 设置 additionalProperties: false")
    return True


def test_required_scopes_validation():
    """测试 required_scopes 字段的约束"""
    schema = load_schema()
    if not schema:
        return False

    source_def = schema['$defs']['source']
    required_scopes_def = source_def['properties'].get('required_scopes')

    if not required_scopes_def:
        print("FAIL: source 缺少 required_scopes 属性定义")
        return False

    # 验证 required_scopes 是数组且有 minItems: 1
    if required_scopes_def.get('type') != 'array':
        print("FAIL: required_scopes 不是 array 类型")
        return False

    if required_scopes_def.get('minItems', 0) < 1:
        print("FAIL: required_scopes 未设置 minItems: 1")
        return False

    # 验证 items 有 enum 限制
    items_def = required_scopes_def.get('items', {})
    if 'enum' not in items_def:
        print("FAIL: required_scopes.items 缺少 enum 限制")
        return False

    # 验证 enum 值来自实际批准 scope
    expected_scopes = {'read_public_pages', 'search_public_web', 'read_public_docs'}
    actual_scopes = set(items_def['enum'])

    if not actual_scopes.issubset(expected_scopes):
        print(f"FAIL: required_scopes.items.enum 包含未批准 scope: {actual_scopes - expected_scopes}")
        return False

    print("PASS: required_scopes 定义正确（array, minItems: 1, enum 限制为批准 scope）")
    return True


def test_examples_valid():
    """测试 schema 中的 examples 能通过验证"""
    if not HAS_JSONSCHEMA:
        print("SKIP: jsonschema not available, cannot validate examples")
        return True

    schema = load_schema()
    if not schema:
        return False

    examples = schema.get('examples', [])
    if not examples:
        print("WARN: Schema 无 examples")
        return True

    passed = 0
    failed = 0

    for i, example in enumerate(examples):
        try:
            jsonschema.validate(instance=example, schema=schema)
            passed += 1
        except jsonschema.ValidationError as e:
            print(f"FAIL: Example {i} 验证失败: {e.message}")
            failed += 1

    if failed > 0:
        return False

    print(f"PASS: 所有 {passed} 个 examples 通过验证")
    return True


def test_invalid_fixtures():
    """测试无效 fixture 应该失败"""
    if not HAS_JSONSCHEMA:
        print("SKIP: jsonschema not available, cannot test invalid fixtures")
        return True

    schema = load_schema()
    if not schema:
        return False

    source_schema = schema['$defs']['source']

    # Fixture 1: 缺少 resource_approval_id
    fixture_missing_approval = {
        "id": "test-source",
        "type": "web",
        "base_url": "https://example.com",
        "access_mode": "public-web-read",
        "required_scopes": ["read_public_pages"],
        "enabled": True
    }

    try:
        jsonschema.validate(instance=fixture_missing_approval, schema=source_schema)
        print("FAIL: 缺少 resource_approval_id 的 fixture 未被拒绝")
        return False
    except jsonschema.ValidationError:
        pass  # 预期失败

    # Fixture 2: 缺少 required_scopes
    fixture_missing_scopes = {
        "id": "test-source",
        "type": "web",
        "base_url": "https://example.com",
        "access_mode": "public-web-read",
        "resource_approval_id": "public-web-read",
        "enabled": True
    }

    try:
        jsonschema.validate(instance=fixture_missing_scopes, schema=source_schema)
        print("FAIL: 缺少 required_scopes 的 fixture 未被拒绝")
        return False
    except jsonschema.ValidationError:
        pass  # 预期失败

    # Fixture 3: 包含未知字段（additionalProperties: false 应拒绝）
    fixture_unknown_field = {
        "id": "test-source",
        "type": "web",
        "base_url": "https://example.com",
        "access_mode": "public-web-read",
        "resource_approval_id": "public-web-read",
        "required_scopes": ["read_public_pages"],
        "enabled": True,
        "unknown_field": "should fail"
    }

    try:
        jsonschema.validate(instance=fixture_unknown_field, schema=source_schema)
        print("FAIL: 包含未知字段的 fixture 未被拒绝")
        return False
    except jsonschema.ValidationError:
        pass  # 预期失败

    print("PASS: 无效 fixtures（缺审批 ID、缺 scope、未知字段）正确失败")
    return True


def test_valid_fixture():
    """测试有效 fixture 应该通过"""
    if not HAS_JSONSCHEMA:
        print("SKIP: jsonschema not available, cannot test valid fixture")
        return True

    schema = load_schema()
    if not schema:
        return False

    source_schema = schema['$defs']['source']

    valid_fixture = {
        "id": "test-source",
        "type": "web",
        "base_url": "https://example.com",
        "access_mode": "public-web-read",
        "resource_approval_id": "public-web-read",
        "required_scopes": ["read_public_pages"],
        "enabled": True,
        "cursor_strategy": "timestamp"
    }

    try:
        jsonschema.validate(instance=valid_fixture, schema=source_schema)
    except jsonschema.ValidationError as e:
        print(f"FAIL: 有效 fixture 验证失败: {e.message}")
        return False

    print("PASS: 有效 fixture 通过验证")
    return True


def test_documentation_consistency():
    """测试面向实施的综合文档不再声称具体来源必须写入 rules/"""
    # 检查 schema 文档
    schema_path = Path(__file__).parent.parent / "exploration" / "scout-source-registry.schema.yaml"
    if not schema_path.exists():
        print(f"FAIL: Schema file not found at {schema_path}")
        return False

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_content = f.read()

    # 验证 schema 文档说明分层
    if "rules/RESOURCE_APPROVALS.yaml 定义批准的能力 scope" not in schema_content:
        print("FAIL: Schema 文档未明确能力 scope 与 registry 分层")
        return False

    if "本 registry 定义具体来源 allowlist" not in schema_content:
        print("FAIL: Schema 文档未明确 registry 定义具体来源")
        return False

    if "在已批准 scope 内新增公开只读来源" not in schema_content:
        print("FAIL: Schema 文档未说明在已批准 scope 内可直接添加来源")
        return False

    # 检查 project candidates 文档
    project_candidates_path = Path(__file__).parent.parent / "proposals" / "project_candidates" / "2026-06-21-autonomous-agent-followups.md"
    if project_candidates_path.exists():
        with open(project_candidates_path, 'r', encoding='utf-8') as f:
            pc_content = f.read()

        # 拒绝明确错误的短语
        if "具体允许来源在 `rules/RESOURCE_APPROVALS.yaml` 中定义" in pc_content:
            print("FAIL: project_candidates 仍声称具体来源在 rules/RESOURCE_APPROVALS.yaml 中定义")
            return False

        # 验证正确的架构描述存在
        if "data/exploration/scout-sources.yaml` 等 registry 实例定义具体来源" not in pc_content:
            print("FAIL: project_candidates 缺少正确的 registry 架构说明")
            return False

    # 检查 daily report 文档
    daily_report_path = Path(__file__).parent.parent / "exploration" / "daily_reports" / "2026-06-21-autonomous-agent-ecosystem.md"
    if daily_report_path.exists():
        with open(daily_report_path, 'r', encoding='utf-8') as f:
            dr_content = f.read()

        if "具体允许来源在 `rules/RESOURCE_APPROVALS.yaml` 中定义" in dr_content:
            print("FAIL: daily_report 仍声称具体来源在 rules/RESOURCE_APPROVALS.yaml 中定义")
            return False

    # 检查 permission proposal 文档
    permission_proposal_path = Path(__file__).parent.parent / "proposals" / "rule_changes" / "2026-06-22-scout-runner-script-permissions.md"
    if permission_proposal_path.exists():
        with open(permission_proposal_path, 'r', encoding='utf-8') as f:
            pp_content = f.read()

        if "具体允许来源在 `rules/RESOURCE_APPROVALS.yaml` 中定义" in pp_content:
            print("FAIL: permission_proposal 仍声称具体来源在 rules/RESOURCE_APPROVALS.yaml 中定义")
            return False

    print("PASS: 所有面向实施的综合文档正确说明能力 scope 与 registry 分层")
    return True


def main():
    """运行所有测试"""
    if not test_dependencies():
        return 1

    tests = [
        ("Schema 结构", test_schema_structure),
        ("Required 字段", test_required_fields),
        ("AdditionalProperties", test_additional_properties),
        ("Required Scopes 验证", test_required_scopes_validation),
        ("Examples 验证", test_examples_valid),
        ("无效 Fixtures", test_invalid_fixtures),
        ("有效 Fixture", test_valid_fixture),
        ("文档一致性", test_documentation_consistency),
    ]

    passed = 0
    failed = 0
    skipped = 0

    print("=" * 60)
    print("Scout Schema 契约测试")
    print("=" * 60)

    for name, test_func in tests:
        print(f"\n测试: {name}")
        try:
            result = test_func()
            if result is None:
                skipped += 1
            elif result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"FAIL: 测试异常: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"结果: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 60)

    if not HAS_JSONSCHEMA:
        print("\n注意: jsonschema 未安装，部分测试被跳过")
        print("完整验证需要: pip install jsonschema")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
