from run_bench_gs82 import _build_parser, run_benchmark


if __name__ == "__main__":
    args = _build_parser().parse_args()
    run_benchmark(gs_path=args.gs_path, output_path=args.output, strict_manifest=args.strict_manifest)
