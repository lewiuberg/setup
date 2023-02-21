#!/usr/bin/env zsh

# Frame text in a box
function frame_text() {
    text="$1"
    echo "┌$(printf "%0.s─" $(seq 1 ${#text}))──┐"
    echo "│ $text │"
    echo "└$(printf "%0.s─" $(seq 1 ${#text}))──┘"
}

# function line() {
#     ORIGINAL_COMMENT="#! ORIGINAL"
#     NEW_COMMENT="#* NEW"
#     #  |||||||||||||||||||||||||||||||| check |||||||||||||||||||||||||||||||||
#     if [[ $1 == "check" ]]; then
#         CHECK_LINE=$2      # "the line to check if exist"
#         WHERE=$3           # is/below/above
#         NAVIGATION_LINE=$4 # anywhere/"The line to check if CEHCK_LINE exist below or above"
#         FILE_KEYWORD=$5    # in
#         FILE=$6            # ~/.p10k.zsh
#         if [[ $WHERE == "is" || $NEW_LINE == "anywhere" ]]; then
#             if grep -qF "$CHECK_LINE" $FILE; then
#                 echo 0
#             else
#                 echo 1
#             fi
#         # *************************** check: below ****************************
#         elif [[ $WHERE == "below" ]]; then
#             if grep -qF "$NAVIGATION_LINE" $FILE; then # true, even if comment is at the end of the line
#                 NAVIGATION_LINE_NUMBER=$(grep -n "$NAVIGATION_LINE" $FILE | cut -d: -f1)
#                 CHECK_LINE_NUMBER_BELOW=$((NAVIGATION_LINE_NUMBER + 1))
#                 CHECK_LINE_FROM_FILE=$(sed -n "$CHECK_LINE_NUMBER_BELOW"p $FILE)
#                 if [[ $CHECK_LINE_FROM_FILE == *"$NEW_COMMENT" ]]; then
#                     CHECK_LINE="$CHECK_LINE $NEW_COMMENT"
#                 elif [[ $CHECK_LINE_FROM_FILE == *"$ORIGINAL_COMMENT" ]]; then
#                     CHECK_LINE="$CHECK_LINE $ORIGINAL_COMMENT"
#                 fi
#                 if [[ "$CHECK_LINE" == "$CHECK_LINE_FROM_FILE" ]]; then
#                     echo 0
#                 else
#                     echo 1
#                 fi
#             else
#                 echo 1
#             fi
#         # *************************** check: above ****************************
#         elif [[ $WHERE == "above" ]]; then
#             if grep -qF "$NAVIGATION_LINE" $FILE; then # true, even if comment is at the end of the line
#                 NAVIGATION_LINE_NUMBER=$(grep -n "$NAVIGATION_LINE" $FILE | cut -d: -f1)
#                 CHECK_LINE_NUMBER_ABOVE=$((NAVIGATION_LINE_NUMBER - 1))
#                 CHECK_LINE_FROM_FILE=$(sed -n "$CHECK_LINE_NUMBER_ABOVE"p $FILE)
#                 if [[ $CHECK_LINE_FROM_FILE == *"$NEW_COMMENT" ]]; then
#                     CHECK_LINE="$CHECK_LINE $NEW_COMMENT"
#                 elif [[ $CHECK_LINE_FROM_FILE == *"$ORIGINAL_COMMENT" ]]; then
#                     CHECK_LINE="$CHECK_LINE $ORIGINAL_COMMENT"
#                 fi
#                 if [[ "$CHECK_LINE" == "$CHECK_LINE_FROM_FILE" ]]; then
#                     echo 0
#                 else
#                     echo 1
#                 fi
#             else
#                 echo 1
#             fi
#         fi
#     #  |||||||||||||||||||||||||||||||| change |||||||||||||||||||||||||||||||||
#     elif [[ $1 == "change" ]]; then
#         ORIGINAL_LINE=$2
#         WHERE=$3
#         MODIFIED_LINE=$4
#         FILE_KEYWORD=$5
#         FILE=$6
#         if [[ $ORIGINAL_LINE == *\n* ]]; then
#             ORIGINAL_LINE=$(echo "$ORIGINAL_LINE" | sed 's/\n/\\n/g')
#         fi
#         if [[ $MODIFIED_LINE == *\n* ]]; then
#             MODIFIED_LINE=$(echo "$MODIFIED_LINE" | sed 's/\n/\\n/g')
#         fi
#         if grep -qF "$(printf '%s' "$ORIGINAL_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE; then
#             ORIGINAL_LINE_FROM_FILE=$(grep -F "$ORIGINAL_LINE" $FILE)
#             if ! [[ $MODIFIED_LINE == *"$NEW_COMMENT" ]]; then
#                 MODIFIED_LINE="$MODIFIED_LINE $NEW_COMMENT"
#             fi
#             if ! [[ $ORIGINAL_LINE_FROM_FILE == *"$ORIGINAL_COMMENT" ]]; then
#                 printf '%s\n' "$ORIGINAL_LINE $ORIGINAL_COMMENT" "$MODIFIED_LINE" | sed -i '' "/$ORIGINAL_LINE/{
#                     r /dev/stdin
#                     d
#                 }" $FILE
#                 echo "Modified:     line change found that '$ORIGINAL_LINE' was not modified in $FILE"
#             else
#                 echo "Not modified: line change found that '$ORIGINAL_LINE' was already modified in $FILE"
#             fi
#         else
#             echo "Not modified: line change did not find '$ORIGINAL_LINE' in $FILE"
#         fi
#     #  ||||||||||||||||||||||||||||||| comment ||||||||||||||||||||||||||||||||
#     elif [[ $1 == "comment" ]]; then
#         MATCH=$2
#         LINE=$3
#         FILE_KEYWORD=$4
#         FILE=$5
#         if grep -qF "$(printf '%s' "$LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE; then
#             LINE_NUMBERS=$(grep -n "$(printf '%s' "$LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
#             INDENTATION=$(echo "$LINE" | grep -o '^[[:space:]]*')
#             if [[ $MATCH == "all" ]]; then
#                 for LINE_NUMBER in $LINE_NUMBERS; do
#                     LINE=$(echo "$LINE" | sed 's/^[[:space:]]*//')
#                     printf '%s\n' "$INDENTATION# $LINE $NEW_COMMENT" | sed -i '' "$LINE_NUMBER{
#                                 r /dev/stdin
#                                 d
#                             }" $FILE
#                 done
#                 echo "Modified:     line comment out found that '$LINE' was not commented out in $FILE"
#             elif [[ $MATCH == "first" ]]; then
#                 LINE_NUMBER=$(echo "$LINE_NUMBERS" | head -n 1)
#                 LINE=$(echo "$LINE" | sed 's/^[[:space:]]*//')
#                 printf '%s\n' "$INDENTATION# $LINE $NEW_COMMENT" | sed -i '' "$LINE_NUMBER{
#                             r /dev/stdin
#                             d
#                         }" $FILE
#                 echo "Modified:     line comment out found that '$LINE' was not commented out in $FILE"
#             fi
#         else
#             echo "Not modified: line comment out did not find '$LINE' in $FILE"
#         fi
#     #  ||||||||||||||||||||||||||||||| uncomment ||||||||||||||||||||||||||||||||
#     elif [[ $1 == "uncomment" ]]; then
#         MATCH=$2
#         LINE=$3
#         FILE_KEYWORD=$4
#         FILE=$5
#         if grep -qF "$(printf '%s' "$LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE; then
#             LINE_NUMBERS=$(grep -n "$(printf '%s' "$LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
#             INDENTATION=$(echo "$LINE" | grep -o '^[[:space:]]*')
#             if [[ $MATCH == "all" ]]; then
#                 for LINE_NUMBER in $LINE_NUMBERS; do
#                     LINE=$(echo "$LINE" | sed 's/^[[:space:]]*# //')
#                     printf '%s\n' "$INDENTATION$LINE $NEW_COMMENT" | sed -i '' "$LINE_NUMBER{
#                                 r /dev/stdin
#                                 d
#                             }" $FILE
#                 done
#                 echo "Modified:     line uncomment out found that '$LINE' was not uncommented out in $FILE"
#             elif [[ $MATCH == "first" ]]; then
#                 LINE_NUMBER=$(echo "$LINE_NUMBERS" | head -n 1)
#                 LINE=$(echo "$LINE" | sed 's/^[[:space:]]*# //')
#                 printf '%s\n' "$INDENTATION$LINE $NEW_COMMENT" | sed -i '' "$LINE_NUMBER{
#                             r /dev/stdin
#                             d
#                         }" $FILE
#                 echo "Modified:     line uncomment out found that '$LINE' was not uncommented out in $FILE"
#             else
#                 echo "Not modified: line uncomment out found that '$LINE' was already uncommented out in $FILE"
#             fi
#         fi
#     #  ||||||||||||||||||||||||||||||||| add ||||||||||||||||||||||||||||||||||
#     elif [[ $1 == "add" ]] && ! [[ $3 == "at" ]]; then
#         NEW_LINE=$2
#         WHERE=$3
#         NAVIGATION_LINE=$4
#         FILE_KEYWORD=$5
#         FILE=$6
#         # NAVIGATION_LINE_NUMBER=$(grep -n "$(printf '%s' "$NAVIGATION_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
#         # NAVIGATION_LINE_NUMBER=$(echo $NAVIGATION_LINE_NUMBER | cut -d' ' -f1)
#         # if [[ $WHERE == "above" ]]; then
#         #     CHECK_LINE_NUMBER_POSITION=$(($NAVIGATION_LINE_NUMBER - 1))
#         # elif [[ $WHERE == "below" ]]; then
#         #     CHECK_LINE_NUMBER_POSITION=$(($NAVIGATION_LINE_NUMBER + 1))
#         # fi
#         # CHECK_LINE_FROM_FILE=$(sed -n "$CHECK_LINE_NUMBER_POSITION"p $FILE)
#         # # CHECK=$(echo $CHECK_LINE_FROM_FILE | sed -e 's/^#//')
#         # # CHECK=$(echo $CHECK | sed -e 's/^[[:space:]]*//')
#         # # combine the above two lines into one
#         # CHECK=$(echo $CHECK_LINE_FROM_FILE | sed -e 's/^#//' -e 's/^[[:space:]]*//')
#         # NEW=$(echo $NEW_LINE | sed -e 's/^[[:space:]]*//')

#         # # if [[ $NEW_LINE == *\n* ]]; then
#         # #     MODIFIED_LINE=$(echo "$NEW_LINE" | sed 's/\n/\\n/g')
#         # #     echo "LEWI:$MODIFIED_LINE"
#         # # else
#         # #     MODIFIED_LINE=$NEW_LINE
#         # # fi
#         # # if ! [[ $MODIFIED_LINE == *"$NEW_COMMENT" ]]; then
#         # #     MODIFIED_LINE="$MODIFIED_LINE $NEW_COMMENT"
#         # # fi
#         # if ! [ $(line check "$NEW_LINE" $WHERE "$NAVIGATION_LINE" $FILE_KEYWORD $FILE) -eq 0 ]; then
#         #     # ************************** add: below ***************************
#         #     # if [[ $WHERE == "below" ]]; then
#         #     # NAVIGATION_LINE_NUMBER=$(grep -n "$(printf '%s' "$NAVIGATION_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
#         #     # # Only keep the first number/match
#         #     # NAVIGATION_LINE_NUMBER=$(echo $NAVIGATION_LINE_NUMBER | cut -d' ' -f1)
#         #     # CHECK_LINE_NUMBER_BELOW=$(($NAVIGATION_LINE_NUMBER + 1))
#         #     # CHECK_LINE_FROM_FILE=$(sed -n "$CHECK_LINE_NUMBER_BELOW"p $FILE)
#         #     # CHECK=$(echo $CHECK_LINE_FROM_FILE | sed -e 's/^#//')
#         #     # CHECK=$(echo $CHECK | sed -e 's/^[[:space:]]*//')
#         #     # NEW=$(echo $NEW_LINE | sed -e 's/^[[:space:]]*//')
#         #     if [[ $CHECK == *"$NEW"* ]] && [[ $CHECK == *"$ORIGINAL_COMMENT" ]]; then
#         #         echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
#         #     else
#         #         # sed -i '' "$CHECK_LINE_NUMBER_POSITION s/^/$NEW_LINE $NEW_COMMENT\n/" $FILE
#         #         # sed -i '' "$CHECK_LINE_NUMBER_POSITION s/^/$MODIFIED_LINE $NEW_COMMENT\n/" $FILE
#         #         printf '%s\n' "$NEW_LINE $NEW_COMMENT" | sed -i '' "$CHECK_LINE_NUMBER_POSITION{
#         #                         r /dev/stdin
#         #                         d
#         #                     }" $FILE
#         #         echo "Modified:     line add added '$NEW_LINE' '$WHERE' '$NAVIGATION_LINE' in $FILE"
#         #     fi
#         #     # # ************************** add: above ***************************
#         #     # elif [[ $WHERE == "above" ]]; then
#         #     #     NAVIGATION_LINE_NUMBER=$(grep -n "$(printf '%s' "$NAVIGATION_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
#         #     #     # Only keep the first number/match
#         #     #     # NAVIGATION_LINE_NUMBER=$(echo $NAVIGATION_LINE_NUMBER | cut -d' ' -f1)
#         #     #     # CHECK_LINE_NUMBER_ABOVE=$(($NAVIGATION_LINE_NUMBER - 1))
#         #     #     # CHECK_LINE_FROM_FILE=$(sed -n "$CHECK_LINE_NUMBER_ABOVE"p $FILE)
#         #     #     # CHECK=$(echo $CHECK_LINE_FROM_FILE | sed -e 's/^#//')
#         #     #     # CHECK=$(echo $CHECK | sed -e 's/^[[:space:]]*//')
#         #     #     # NEW=$(echo $NEW_LINE | sed -e 's/^[[:space:]]*//')
#         #     #     if [[ $CHECK == *"$NEW"* ]] && [[ $CHECK == *"$ORIGINAL_COMMENT" ]]; then
#         #     #         echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
#         #     #     else
#         #     #         # sed -i '' "$CHECK_LINE_NUMBER_POSITION s/^/$NEW_LINE $NEW_COMMENT\n/" $FILE

#         #     #         echo "Modified:     line add added '$NEW_LINE' above '$NAVIGATION_LINE' in $FILE"
#         #     #     fi
#         #     # fi
#         # else
#         #     echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
#         # fi
#         NAVIGATION_LINE_NUMBER=$(grep -n "$(printf '%s' "$NAVIGATION_LINE" | sed 's/[]\/$*.^|[]/\\&/g')" $FILE | cut -d: -f1)
#         NAVIGATION_LINE_NUMBER=$(echo $NAVIGATION_LINE_NUMBER | cut -d' ' -f1)
#         echo "LEWI: $NAVIGATION_LINE_NUMBER"
#         if [[ $WHERE == "below" ]]; then
#             CHECK_LINE_NUMBER_POSITION=$(($NAVIGATION_LINE_NUMBER + 1))
#         elif [[ $WHERE == "above" ]]; then
#             CHECK_LINE_NUMBER_POSITION=$(($NAVIGATION_LINE_NUMBER - 1))
#         fi
#         CHECK_LINE_FROM_FILE=$(sed -n "$CHECK_LINE_NUMBER_POSITION"p $FILE)
#         echo "LEWI:$CHECK_LINE_FROM_FILE"
#         # if ! [ $(line check "$NEW_LINE" $WHERE "$NAVIGATION_LINE" $FILE_KEYWORD $FILE) -eq 0 ]; then
#         #     echo "N:$NEW_LINE"
#         #     echo "C:$CHECK_LINE_FROM_FILE"
#         # else
#         #     echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
#         # if "    os_icon                 # os identifier" is below "    # =========================[ Line #1 ]=========================", echo "line is below"
#         if [[ $CHECK_LINE_FROM_FILE == *"$NEW_LINE"* ]]; then
#             echo "line is below"
#             # if NEW_COMMENT or ORIGINAL_COMMENT is in CHECK_LINE_FROM_FILE, echo "but already modified"
#             if [[ $CHECK_LINE_FROM_FILE == *"$NEW_COMMENT"* ]] || [[ $CHECK_LINE_FROM_FILE == *"$ORIGINAL_COMMENT"* ]]; then
#                 echo "but already modified"
#             else
#                 # if NEW_COMMENT is not in CHECK_LINE_FROM_FILE, echo "but not modified"
#                 echo "but not modified"
#             fi
#         else
#             echo "line is not below"
#             sed -i '' "$CHECK_LINE_NUMBER_POSITION s/^/$NEW_LINE $NEW_COMMENT\n/" $FILE
#         fi
#     # ************************** add: at ***************************
#     elif [[ $1 == "add" ]] && [[ $3 == "at" ]]; then
#         NEW_LINE=$2
#         KEYWORD_1=$3
#         WHERE=$4 # Beginning or end of file
#         KEYWORD_2=$5
#         FILE=$6
#         # ************************** add: at: start ***************************
#         if [[ $WHERE == "start" ]]; then
#             CHECK_LINE=$(sed -n 1p $FILE)
#             if [[ $CHECK_LINE == "$NEW_LINE $NEW_COMMENT" ]] || [[ $CHECK_LINE == "$NEW_LINE" ]] || [[ $CHECK_LINE == "$NEW_LINE $ORIGINAL_COMMENT" ]]; then
#                 echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
#             else
#                 sed -i '' "1s/^/$NEW_LINE $NEW_COMMENT\n/" $FILE
#                 echo "Modified:     line add added '$NEW_LINE' at the start of $FILE"
#             fi
#         fi
#         # ************************** add: at: end ***************************
#         if [[ $WHERE == "end" ]]; then
#             CHECK_LINE=$(sed -n '$p' $FILE)
#             if [[ $CHECK_LINE == "$NEW_LINE $NEW_COMMENT" ]] || [[ $CHECK_LINE == "$NEW_LINE" ]] || [[ $CHECK_LINE == "$NEW_LINE $ORIGINAL_COMMENT" ]]; then
#                 echo "Not modified: line add found that '$NEW_LINE' was already modified in $FILE"
#             else
#                 sed -i '' "\$s/\$/\n$NEW_LINE $NEW_COMMENT/" $FILE
#                 echo "Modified:     line add added '$NEW_LINE' at the end of $FILE"
#             fi
#         fi
#     fi
#     # ||||||||||||||||||||||||||||||||| remove ||||||||||||||||||||||||||||||||||
#     if [[ $1 == "remove" ]]; then
#         # ************************** remove: line ***************************
#         if [[ $2 == "line" ]]; then
#             LINE_NUMBER=$3
#             FILE_KEYWORD=$4
#             FILE=$5
#             CHECK_LINE_FROM_FILE=$(sed -n "$LINE_NUMBER"p $FILE)
#             if [[ $CHECK_LINE_FROM_FILE == "" ]]; then
#                 echo "Not modified: line remove found that line $LINE_NUMBER does not exist in $FILE"
#             else
#                 sed -i '' "$LINE_NUMBER d" $FILE
#                 echo "Modified:     line remove removed line $LINE_NUMBER from $FILE"
#             fi
#         # ************************** remove: range ***************************
#         elif [[ $2 == "range" ]]; then
#             RANGE_START=$3
#             RANGE_KEYWORD=$4
#             RANGE_END=$5
#             FILE_KEYWORD=$6
#             FILE=$7
#             if [[ $RANGE_START == "start" ]]; then
#                 RANGE_START=1
#             fi
#             if [[ $RANGE_END == "end" ]]; then
#                 RANGE_END=$(wc -l <$FILE)
#             fi
#             sed -i '' "$RANGE_START,$RANGE_END d" $FILE
#             echo "Modified:     line remove removed range $RANGE_START to $RANGE_END from $FILE"
#         # ************************** remove: all found ***************************
#         elif [[ $2 == "all" ]] && [[ $3 == "found" ]]; then
#             LINE=$4
#             FILE_KEYWORD=$5
#             FILE=$6
#             LINES_NUMBERS=$(grep -Fn "$LINE" $FILE | cut -d: -f1)
#             LINES_NUMBERS=$(echo "$LINES_NUMBERS" | tac)
#             echo "$LINES_NUMBERS"
#             while read -r line; do
#                 sed -i '' "$line d" $FILE
#             done <<<"$LINES_NUMBERS"
#         # ************************** remove: first found ***************************
#         elif [[ $2 == "first" ]] && [[ $3 == "found" ]]; then
#             LINE=$4
#             FILE_KEYWORD=$5
#             FILE=$6
#             if grep -qF "$LINE" $FILE; then
#                 LINE_NUMBER=$(grep -Fn "$LINE" $FILE | head -n 1 | cut -d: -f1)
#                 sed -i '' "$LINE_NUMBER d" $FILE
#                 echo "Modified:     line remove removed first found '$LINE' from $FILE"
#             else
#                 echo "Not modified: line remove found that '$LINE' was already removed from $FILE"
#             fi
#         # ************************** remove: last found ***************************
#         elif [[ $2 == "last" ]] && [[ $3 == "found" ]]; then
#             LINE=$4
#             FILE_KEYWORD=$5
#             FILE=$6
#             if grep -qF "$LINE" $FILE; then
#                 LINE_NUMBER=$(grep -Fn "$LINE" $FILE | tail -n 1 | cut -d: -f1)
#                 sed -i '' "$LINE_NUMBER d" $FILE
#                 echo "Modified:     line remove removed last found '$LINE' from $FILE"
#             else
#                 echo "Not modified: line remove found that '$LINE' was already removed from $FILE"
#             fi
#         fi
#         # ||||||||||||||||||||||||||||||||| append ||||||||||||||||||||||||||||||||||
#     elif [[ $1 == "append" ]]; then
#         APPEND=$2
#         KEYWORD_1=$3
#         WHERE=$4
#         LINE=$5
#         FILE_KEYWORD=$6
#         FILE=$7
#         LINES_NUMBERS=$(grep -Fn "$LINE" $FILE | cut -d: -f1)
#         echo "$LINES_NUMBERS"
#         # ************************** append: to first found ***************************
#         if [[ $WHERE == "first" ]]; then
#             LINE_NUMBER=$(grep -Fn "$LINE" $FILE | head -n 1 | cut -d: -f1)
#             CHECK_LINE_FROM_FILE=$(sed -n "$LINE_NUMBER"p $FILE)
#             if [[ $CHECK_LINE_FROM_FILE == "" ]]; then
#                 echo "Not modified: line append found that line $LINE_NUMBER does not exist in $FILE"
#             else
#                 sed -i '' "$LINE_NUMBER s/$/ $APPEND/" $FILE
#                 echo "Modified:     line append appended '$APPEND' to first found '$LINE' in $FILE"
#             fi
#         fi
#         # ************************** append: to last found ***************************
#         if [[ $WHERE == "last" ]]; then
#             LINE_NUMBER=$(grep -Fn "$LINE" $FILE | tail -n 1 | cut -d: -f1)
#             CHECK_LINE_FROM_FILE=$(sed -n "$LINE_NUMBER"p $FILE)
#             if [[ $CHECK_LINE_FROM_FILE == "" ]]; then
#                 echo "Not modified: line append found that line $LINE_NUMBER does not exist in $FILE"
#             else
#                 sed -i '' "$LINE_NUMBER s/$/ $APPEND/" $FILE
#                 echo "Modified:     line append appended '$APPEND' to last found '$LINE' in $FILE"
#             fi
#         fi
#         # ************************** append: to all found ***************************
#         if [[ $WHERE == "all" ]]; then
#             while read -r line; do
#                 CHECK_LINE_FROM_FILE=$(sed -n "$line"p $FILE)
#                 if [[ $CHECK_LINE_FROM_FILE == "" ]]; then
#                     echo "Not modified: line append found that line $line does not exist in $FILE"
#                 else
#                     sed -i '' "$line s/$/ $APPEND/" $FILE
#                     echo "Modified:     line append appended '$APPEND' to line $line in $FILE"
#                 fi
#             done <<<"$LINES_NUMBERS"
#         fi
#     # ||||||||||||||||||||||||||||||||| help ||||||||||||||||||||||||||||||||||
#     elif [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; then
#         echo "Usage: line [OPTION] [ARGUMENT]+"
#         echo "Options:"
#         echo "  check [STRING] below [STRING] in [FILE]"
#         echo "  check [STRING] above [STRING] in [FILE]"
#         echo "  change [STRING] to [STRING] in [FILE]"
#         echo "  add [STRING] below [STRING] in [FILE]"
#         echo "  add [STRING] above [STRING] in [FILE]"
#         echo "  add [STRING] at start of [FILE]"
#         echo "  add [STRING] at end of [FILE]"
#         echo "  remove line [NUMBER] from [FILE]"
#         echo "  remove range [NUMBER] to [NUMBER] from [FILE]"
#         echo "  remove range [NUMBER] to end from [FILE]"
#         echo "  remove range start to [NUMBER] from [FILE]"
#         echo "  remove range start to end from [FILE]"
#         echo "  remove all found [STRING] from [FILE]"
#         echo "  remove first found [STRING] from [FILE]"
#         echo "  remove last found [STRING] from [FILE]"
#         echo "  append [STRING] to first [STRING] in [FILE]"
#         echo "  append [STRING] to last [STRING] in [FILE]"
#         echo "  append [STRING] to all [STRING] in [FILE]"
#         echo "  comment all [STRING] in [FILE]"
#         echo "  comment first [STRING] in [FILE]"
#         echo "  uncomment all [STRING] in [FILE]"
#         echo "  uncomment first [STRING] in [FILE]"
#         echo "  -h or --help"
#         echo "Examples:"
#         echo "  line check \"string 1\" below \"string 2\" in ~/.p10k.zsh"
#         echo "  line check \"string 1\" above \"string 2\" in ~/.p10k.zsh"
#         echo "  line change \"string 1\" to \"string 2\" in ~/.p10k.zsh"
#         echo "  line add \"string 1\" below \"string 2\" in ~/.p10k.zsh"
#         echo "  line add \"string 1\" above \"string 2\" in ~/.p10k.zsh"
#         echo "  line add \"string 1\" at start of ~/.p10k.zsh"
#         echo "  line add \"string 1\" at end of ~/.p10k.zsh"
#         echo "  line remove line 1765 from ~/.p10k.zsh"
#         echo "  line remove range 2 to 16 from ~/.p10k.zsh"
#         echo "  line remove range 1750 to end in ~/.p10k.zsh"
#         echo "  line remove range start to 3 from ~/.p10k.zsh"
#         echo "  line remove range start to end from ~/.p10k.zsh"
#         echo "  line remove all found \"string 1\" from ~/.p10k.zsh"
#         echo "  line remove first found \"string 1\" from ~/.p10k.zsh"
#         echo "  line remove last found \"string 1\" from ~/.p10k.zsh"
#         echo "  line append \"string 1\" to first \"string 2\" in ~/.p10k.zsh"
#         echo "  line append \"string 1\" to last \"string 2\" in ~/.p10k.zsh"
#         echo "  line append \"string 1\" to all \"string 2\" in ~/.p10k.zsh"
#         echo "  line comment all \"string 1\" in ~/.p10k.zsh"
#         echo "  line comment first \"string 1\" in ~/.p10k.zsh"
#         echo "  line uncomment all \"# string 1\" in ~/.p10k.zsh"
#         echo "  line uncomment first \"# string 1\" in ~/.p10k.zsh"
#         echo "  line -h or line --help"
#     fi
# }

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
            echo "!!!!"
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
        if ! [ $(line check "$NEW_LINE" $WHERE "$NAVIGATION_LINE" $FILE_KEYWORD $FILE) -eq 0 ]; then
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
