#!/usr/bin/env zsh

# Frame text in a box
function frame_text() {
    text="$1"
    echo "┌$(printf "%0.s─" $(seq 1 ${#text}))──┐"
    echo "│ $text │"
    echo "└$(printf "%0.s─" $(seq 1 ${#text}))──┘"
}

function line() {
    ORIGINAL_COMMENT="#! ORIGINAL"
    MODIFIED_COMMENT="#* MODIFIED"
    # ||||||||||||||||||||||||||||||||| check |||||||||||||||||||||||||||||||||
    if [[ $1 == "check" ]]; then
        CHECK_LINE=$2
        WHERE=$3
        if [[ $WHERE == "anywhere" ]]; then
            FILE_KEYWORD=$4
            FILE=$5
            if grep -qF "$CHECK_LINE" "$FILE"; then
                CHECK_LINE_NUMBER=$(grep -n "$(printf '%s' "$CHECK_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
                CHECK_LINE_NUMBER=$(echo $CHECK_LINE_NUMBER | cut -d' ' -f1)
                CHECK_LINE_FROM_FILE=$(sed -n "$CHECK_LINE_NUMBER p" "$FILE")
                if [[ "$(printf '%s' "$CHECK_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" == "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/[]\/$*.^|[]/\\&/g')" ]] || [[ "$(printf '%s' "$CHECK_LINE $ORIGINAL_COMMENT" | sed 's/[]\/$*.^|[]/\\&/g')" == "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/[]\/$*.^|[]/\\&/g')" ]] || [[ "$(printf '%s' "$CHECK_LINE $MODIFIED_COMMENT" | sed 's/[]\/$*.^|[]/\\&/g')" == "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/[]\/$*.^|[]/\\&/g')" ]]; then
                    echo 0
                else
                    echo 1
                fi
            else
                echo 1
            fi
        elif [[ $WHERE == "below" ]]; then
            NAVIGATION_LINE=$4
            FILE_KEYWORD=$5
            FILE=$6
            if grep -qF "$NAVIGATION_LINE" "$FILE"; then
                NAVIGATION_LINE_NUMBER=$(grep -n "$(printf '%s' "$NAVIGATION_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
                NAVIGATION_LINE_NUMBER=$(echo $NAVIGATION_LINE_NUMBER | cut -d' ' -f1)
                CHECK_LINE_NUMBER=$((NAVIGATION_LINE_NUMBER + 1))
                CHECK_LINE_FROM_FILE=$(sed -n "$CHECK_LINE_NUMBER p" "$FILE")
                if [[ "$(printf '%s' "$CHECK_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" == "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/[]\/$*.^|[]/\\&/g')" ]] || [[ "$(printf '%s' "$CHECK_LINE $ORIGINAL_COMMENT" | sed 's/[]\/$*.^|[]/\\&/g')" == "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/[]\/$*.^|[]/\\&/g')" ]] || [[ "$(printf '%s' "$CHECK_LINE $MODIFIED_COMMENT" | sed 's/[]\/$*.^|[]/\\&/g')" == "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/[]\/$*.^|[]/\\&/g')" ]]; then
                    echo 0
                else
                    echo 1
                fi
            else
                echo 1
            fi
        elif [[ $WHERE == "above" ]]; then
            NAVIGATION_LINE=$4
            FILE_KEYWORD=$5
            FILE=$6
            if grep -qF "$NAVIGATION_LINE" "$FILE"; then
                NAVIGATION_LINE_NUMBER=$(grep -n "$(printf '%s' "$NAVIGATION_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
                NAVIGATION_LINE_NUMBER=$(echo $NAVIGATION_LINE_NUMBER | cut -d' ' -f1)
                CHECK_LINE_NUMBER=$((NAVIGATION_LINE_NUMBER - 1))
                CHECK_LINE_FROM_FILE=$(sed -n "$CHECK_LINE_NUMBER p" "$FILE")
                if [[ "$(printf '%s' "$CHECK_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" == "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/[]\/$*.^|[]/\\&/g')" ]] || [[ "$(printf '%s' "$CHECK_LINE $ORIGINAL_COMMENT" | sed 's/[]\/$*.^|[]/\\&/g')" == "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/[]\/$*.^|[]/\\&/g')" ]] || [[ "$(printf '%s' "$CHECK_LINE $MODIFIED_COMMENT" | sed 's/[]\/$*.^|[]/\\&/g')" == "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/[]\/$*.^|[]/\\&/g')" ]]; then
                    echo 0
                else
                    echo 1
                fi
            else
                echo 1
            fi
        fi
    # ||||||||||||||||||||||||||||||||| remove ||||||||||||||||||||||||||||||||||
    elif [[ $1 == "remove" ]]; then
        # ************************** remove: line ***************************
        if [[ $2 == "line" ]]; then
            LINE_NUMBER=$3
            FILE_KEYWORD=$4
            FILE=$5
            CHECK_LINE_FROM_FILE=$(sed -n "$LINE_NUMBER"p $FILE)
            if [[ $CHECK_LINE_FROM_FILE == "" ]]; then
                echo "Not modified: line remove found that line $LINE_NUMBER does not exist in $FILE"
            else
                sed -i '' "$LINE_NUMBER d" $FILE
                echo "Modified:     line remove removed line $LINE_NUMBER from $FILE"
            fi
        # ************************** remove: range ***************************
        elif [[ $2 == "range" ]]; then
            RANGE_START=$3
            RANGE_KEYWORD=$4
            RANGE_END=$5
            FILE_KEYWORD=$6
            FILE=$7
            if [[ $RANGE_START == "start" ]]; then
                RANGE_START=1
            fi
            if [[ $RANGE_END == "end" ]]; then
                RANGE_END=$(wc -l <$FILE)
            fi
            sed -i '' "$RANGE_START,$RANGE_END d" $FILE
            echo "Modified:     line remove removed range $RANGE_START to $RANGE_END from $FILE"
        # ************************** remove: all found ***************************
        elif [[ $2 == "all" ]] && [[ $3 == "found" ]]; then
            LINE=$4
            FILE_KEYWORD=$5
            FILE=$6
            if grep -qF "$LINE" $FILE; then
                LINES_NUMBERS=$(grep -Fn "$LINE" $FILE | cut -d: -f1)
                LINES_NUMBERS=$(echo "$LINES_NUMBERS" | tac)
                while read -r line; do
                    sed -i '' "$line d" $FILE
                done <<<"$LINES_NUMBERS"
                echo "Modified:     line remove removed all found '$LINE' from $FILE"
            else
                echo "Not modified: line remove found that '$LINE' was already removed from $FILE"
            fi
        # ************************** remove: first found ***************************
        elif [[ $2 == "first" ]] && [[ $3 == "found" ]]; then
            LINE=$4
            FILE_KEYWORD=$5
            FILE=$6
            if grep -qF "$LINE" $FILE; then
                LINE_NUMBER=$(grep -Fn "$LINE" $FILE | head -n 1 | cut -d: -f1)
                sed -i '' "$LINE_NUMBER d" $FILE
                echo "Modified:     line remove removed first found '$LINE' from $FILE"
            else
                echo "Not modified: line remove found that '$LINE' was already removed from $FILE"
            fi
        # ************************** remove: last found ***************************
        elif [[ $2 == "last" ]] && [[ $3 == "found" ]]; then
            LINE=$4
            FILE_KEYWORD=$5
            FILE=$6
            if grep -qF "$LINE" $FILE; then
                LINE_NUMBER=$(grep -Fn "$LINE" $FILE | tail -n 1 | cut -d: -f1)
                sed -i '' "$LINE_NUMBER d" $FILE
                echo "Modified:     line remove removed last found '$LINE' from $FILE"
            else
                echo "Not modified: line remove found that '$LINE' was already removed from $FILE"
            fi
        fi
    # ||||||||||||||||||||||||||||||||| replace ||||||||||||||||||||||||||||||||||
    elif [[ $1 == "replace" ]]; then
        WHERE=$2
        ORIGINAL_LINE=$3
        KEYWORD=$4
        MODIFIED_LINE=$5
        FILE_KEYWORD=$6
        FILE=$7
        count=0
        LINE_NUMBERS=()
        NUMBER_OF_LINES=0
        if grep -qF "$ORIGINAL_LINE" $FILE; then
            TEMP_LINE_NUMBERS=$(grep -Fn "$ORIGINAL_LINE" $FILE | cut -d: -f1)

            while read -r line; do
                CHECK_LINE_FROM_FILE=$(sed -n "$line p" "$FILE")
                if ! [[ "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/$ORIGINAL_COMMENT//g')" == *"$ORIGINAL_COMMENT"* ]] && ! [[ "$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/#\*$MODIFIED_COMMENT//g')" == *"$MODIFIED_COMMENT"* ]]; then
                    if ! [[ $LINE_NUMBERS == "" ]]; then
                        NUMBER_OF_LINES=$((NUMBER_OF_LINES + 1))
                        line=$((line + $NUMBER_OF_LINES))
                        LINE_NUMBERS="$LINE_NUMBERS $line"
                    else
                        LINE_NUMBERS="$line"
                    fi
                fi
            done <<<"$TEMP_LINE_NUMBERS"

            for line in $LINE_NUMBERS; do
                sed -i '' "$line s/$(printf '%s' "$CHECK_LINE_FROM_FILE" | sed 's/[]\/$*.^|[]/\\&/g')/$(printf '%s' "$ORIGINAL_LINE $ORIGINAL_COMMENT" | sed 's/[]\/$*.^|[]/\\&/g')\n$(printf '%s' "$MODIFIED_LINE $MODIFIED_COMMENT" | sed 's/[]\/$*.^|[]/\\&/g')/" $FILE
                echo "Modified:     line replace replaced '$ORIGINAL_LINE' with '$MODIFIED_LINE' in $FILE"
                if [[ $WHERE == "first" ]]; then
                    break
                fi
            done
        else
            echo "Not modified: line replace did not find '$ORIGINAL_LINE' in $FILE"
        fi
    #  ||||||||||||||||||||||||||||||| comment ||||||||||||||||||||||||||||||||
    elif [[ $1 == "comment" ]]; then
        MATCH=$2
        LINE=$3
        FILE_KEYWORD=$4
        FILE=$5
        if grep -qF "$(printf '%s' "$LINE" | sed 's/\n[]\/$*.^|[]/\\&/g')" $FILE; then
            LINE_NUMBERS=$(grep -n "$(printf '%s' "$LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
            INDENTATION=$(echo "$LINE" | grep -o '^[[:space:]]*')
            if [[ $MATCH == "all" ]]; then
                for LINE_NUMBER in $LINE_NUMBERS; do
                    LINE=$(echo "$LINE" | sed 's/^[[:space:]]*//')
                    printf '%s\n' "$INDENTATION# $LINE $MODIFIED_COMMENT" | sed -i '' "$LINE_NUMBER{
                                    r /dev/stdin
                                    d
                                }" $FILE
                done
                echo "Modified:     line comment out found that '$LINE' was not commented out in $FILE"
            elif [[ $MATCH == "first" ]]; then
                LINE_NUMBER=$(echo "$LINE_NUMBERS" | head -n 1)
                LINE=$(echo "$LINE" | sed 's/^[[:space:]]*//')
                printf '%s\n' "$INDENTATION# $LINE $MODIFIED_COMMENT" | sed -i '' "$LINE_NUMBER{
                                r /dev/stdin
                                d
                            }" $FILE
                echo "Modified:     line comment out found that '$LINE' was not commented out in $FILE"
            fi
        else
            echo "Not modified: line comment out did not find '$LINE' in $FILE"
        fi
    #  ||||||||||||||||||||||||||||||| uncomment ||||||||||||||||||||||||||||||||
    elif [[ $1 == "uncomment" ]]; then
        MATCH=$2
        LINE=$3
        FILE_KEYWORD=$4
        FILE=$5
        if grep -qF "$(printf '%s' "$LINE" | sed 's/\n[]\/$*.^|[]/\\&/g')" $FILE; then
            LINE_NUMBERS=$(grep -n "$(printf '%s' "$LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
            INDENTATION=$(echo "$LINE" | grep -o '^[[:space:]]*')
            if [[ $MATCH == "all" ]]; then
                for LINE_NUMBER in $LINE_NUMBERS; do
                    LINE=$(echo "$LINE" | sed 's/^[[:space:]]*# //')
                    printf '%s\n' "$INDENTATION$LINE $MODIFIED_COMMENT" | sed -i '' "$LINE_NUMBER{
                                    r /dev/stdin
                                    d
                                }" $FILE
                done
                echo "Modified:     line uncomment out found that '$LINE' was not uncommented out in $FILE"
            elif [[ $MATCH == "first" ]]; then
                LINE_NUMBER=$(echo "$LINE_NUMBERS" | head -n 1)
                LINE=$(echo "$LINE" | sed 's/^[[:space:]]*# //')
                printf '%s\n' "$INDENTATION$LINE $MODIFIED_COMMENT" | sed -i '' "$LINE_NUMBER{
                                r /dev/stdin
                                d
                            }" $FILE
                echo "Modified:     line uncomment out found that '$LINE' was not uncommented out in $FILE"
            else
                echo "Not modified: line uncomment out found that '$LINE' was already uncommented out in $FILE"
            fi
        fi
    #  ||||||||||||||||||||||||||||||||| add ||||||||||||||||||||||||||||||||||
    elif [[ $1 == "add" ]] && ! [[ $3 == "at" ]]; then
        NEW_LINE=$2
        WHERE=$3
        NAVIGATION_LINE=$4
        FILE_KEYWORD=$5
        FILE=$6
        if ! [ $(line check "$NEW_LINE" $WHERE "$NAVIGATION_LINE" $FILE_KEYWORD $FILE) -eq 0 ] && grep -qF "$(printf '%s' "$NAVIGATION_LINE" | sed 's/\n[]\/$*.^|[]/\\&/g')" $FILE; then
            # ************************** add: below ***************************
            if [[ $WHERE == "below" ]]; then
                NAVIGATION_LINE_NUMBER=$(grep -n "$(printf '%s' "$NAVIGATION_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
                # Only keep the first number/match
                NAVIGATION_LINE_NUMBER=$(echo $NAVIGATION_LINE_NUMBER | cut -d' ' -f1)
                CHECK_LINE_NUMBER_BELOW=$(($NAVIGATION_LINE_NUMBER + 1))
                CHECK_LINE_FROM_FILE=$(sed -n "$CHECK_LINE_NUMBER_BELOW"p $FILE)
                CHECK=$(echo $CHECK_LINE_FROM_FILE | sed -e 's/^#//')
                CHECK=$(echo $CHECK | sed -e 's/^[[:space:]]*//')
                NEW=$(echo $NEW_LINE | sed -e 's/^[[:space:]]*//')
                if [[ $CHECK == *"$NEW"* ]] && [[ $CHECK == *"$ORIGINAL_COMMENT" ]]; then
                    echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
                else
                    sed -i '' "$CHECK_LINE_NUMBER_BELOW s/^/\n/" $FILE
                    printf '%s\n' "$NEW_LINE $MODIFIED_COMMENT" | sed -i '' "$CHECK_LINE_NUMBER_BELOW{
                                    r /dev/stdin
                                    d
                                }" $FILE
                    echo "Modified:     line add added '$NEW_LINE' below '$NAVIGATION_LINE' in $FILE"
                fi
            # ************************** add: above ***************************
            elif [[ $WHERE == "above" ]]; then
                NAVIGATION_LINE_NUMBER=$(grep -n "$(printf '%s' "$NAVIGATION_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
                # Only keep the first number/match
                NAVIGATION_LINE_NUMBER=$(echo $NAVIGATION_LINE_NUMBER | cut -d' ' -f1)
                CHECK_LINE_FROM_FILE=$(sed -n "$NAVIGATION_LINE_NUMBER"p $FILE)
                CHECK=$(echo $CHECK_LINE_FROM_FILE | sed -e 's/^#//')
                CHECK=$(echo $CHECK | sed -e 's/^[[:space:]]*//')
                NEW=$(echo $NEW_LINE | sed -e 's/^[[:space:]]*//')
                if [[ $CHECK == *"$NEW"* ]] && [[ $CHECK == *"$ORIGINAL_COMMENT" ]]; then
                    echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
                else
                    sed -i '' "$NAVIGATION_LINE_NUMBER s/^/\n/" $FILE
                    printf '%s\n' "$NEW_LINE $MODIFIED_COMMENT" | sed -i '' "$NAVIGATION_LINE_NUMBER{
                                    r /dev/stdin
                                    d
                                }" $FILE
                    echo "Modified:     line add added '$NEW_LINE' above '$NAVIGATION_LINE' in $FILE"
                fi
            fi
        else
            echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
        fi
    # ************************** add: at ***************************
    elif [[ $1 == "add" ]] && [[ $3 == "at" ]]; then
        NEW_LINE=$2
        KEYWORD_1=$3
        WHERE=$4 # Beginning or end of file
        KEYWORD_2=$5
        FILE=$6
        # ************************** add: at: start ***************************
        if [[ $WHERE == "start" ]]; then
            CHECK_LINE=$(sed -n 1p $FILE)
            if [[ $CHECK_LINE == "$NEW_LINE $MODIFIED_COMMENT" ]] || [[ $CHECK_LINE == "$NEW_LINE" ]] || [[ $CHECK_LINE == "$NEW_LINE $ORIGINAL_COMMENT" ]]; then
                echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
            else
                sed -i '' "1s/^/$NEW_LINE $MODIFIED_COMMENT\n/" $FILE
                echo "Modified:     line add added '$NEW_LINE' at the start of $FILE"
            fi
        fi
        # ************************** add: at: end ***************************
        if [[ $WHERE == "end" ]]; then
            CHECK_LINE=$(sed -n '$p' $FILE)
            if [[ $CHECK_LINE == "$NEW_LINE $MODIFIED_COMMENT" ]] || [[ $CHECK_LINE == "$NEW_LINE" ]] || [[ $CHECK_LINE == "$NEW_LINE $ORIGINAL_COMMENT" ]]; then
                echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
            else
                sed -i '' "\$s/\$/\n$NEW_LINE $MODIFIED_COMMENT/" $FILE
                echo "Modified:     line add added '$NEW_LINE' at the end of $FILE"
            fi
        fi
    fi
}
