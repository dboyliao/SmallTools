#!/usr/bin/env julia --startup-file=no --history-file=no
using IJulia
using ArgParse

function parse_cmdline()
    s = ArgParseSettings(description = "install current environment as kernel")
    @add_arg_table! s begin
        "--path"
            help = "the path of the environment dir"
            default = pwd()
        "--name"
            required = true
            help = "the name of the kernel"
    end

    args = parse_args(s)
    return args
end

function main()
    args = parse_cmdline()
    name = args["name"]
    path = args["path"]
    installkernel(name, "--project=$(path)")
end

if nameof(@__MODULE__) == :Main
    main()
end
