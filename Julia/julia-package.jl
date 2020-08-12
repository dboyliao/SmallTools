#!/usr/bin/env julia --startup-file=no --history-file=no
using PkgTemplates
using ArgParse

function parse_commandline()
    s = ArgParseSettings(description="create julia packge with PkgTemplates");
    @add_arg_table! s begin
        "--user"
            arg_type = String
        "--authors"
            nargs= '?'
            arg_type = Vector{String}
        "--dir"
            default = "."
            arg_type = String
        "--host"
            default = "github.com"
            arg_type = String
        "--julia"
            default = VERSION
            arg_type = VersionNumber
        "project_name"
            arg_type = String
    end
    args = parse_args(s)
    project_name = pop!(args, "project_name")
    valid_args = Dict{Symbol, Any}()
    for (k, v) in args
        if v !== nothing
            valid_args[Symbol(k)] = v
        end
    end
    return project_name, valid_args
end

function main()
    project_name, args = parse_commandline()
    t = Template(;args...)
    t(project_name)
end

if nameof(@__MODULE__) == :Main
    main()
end
