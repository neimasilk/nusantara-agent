# Archive Policy

Folder ini menampung dokumen historis yang masih bernilai audit tetapi tidak lagi menjadi sumber operasional utama.

## Aturan Singkat

1. Dokumen status aktif tetap berada di `docs/` root.
2. Dokumen handoff sementara, context reset, atau prompt transfer sesi dipindahkan ke archive.
3. Jangan hapus artefak histori riset kecuali ada keputusan eksplisit.

## Sumber Operasional Utama Saat Ini

1. `CLAUDE.md`
2. `docs/task_registry.md`
3. `docs/methodology_fixes.md`
4. `docs/failure_registry.md`
5. `docs/review_protocol.md`
6. `docs/testing_framework.md`

## Isi Archive

- `handoffs/` — Dokumen handoff sesi (bertanggal), prompt transfer antar-agent.
- `*-YYYY-MM-DD.md` — Audit log, review snapshot, readiness check historis.
