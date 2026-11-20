# D4.8 V2 pin typo — V1 auditor incident

The V1 auditor embedded an incorrect expected SHA string:

`0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28cdad59301c8f3208239c07`

The actual active file reported 12,996 bytes and SHA-256:

`0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`

The V2 auditor pins only the latter. This is an auditor constant correction. It must not write, replace, normalize or otherwise touch the D4.8 JSON. Its immutable blocked state is preserved.
