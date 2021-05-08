#!/usr/bin/env julia --project=. --startup-file=no
import ArgParse


function main(;mod_name, editor = "code")
    mod = eval(Meta.parse("import $(mod_name); $(mod_name)"))
    mod_path = (
        pathof(mod) # mod.jl
        |> dirname # src
        |> dirname # package dir
    )
    run(`$(editor) $(mod_path)`)
end

if nameof(@__MODULE__) == :Main
    s = ArgParse.ArgParseSettings()
    ArgParse.@add_arg_table! s begin
        "mod_name"
        metavar="MODULE_NAME"
        help = "the module to be edit"
        "--editor"
        help = "the editor to use"
        metavar = "EDITOR_CMD"
        default = "code"
    end
    args = ArgParse.parse_args(s, as_symbols=true)
    main(; args...)
end