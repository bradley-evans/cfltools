_cfltools_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _CFLTOOLS_COMPLETE=complete $1 ) )
    return 0
}

complete -F _cfltools_completion -o default cfltools;
