# semantic_dual_task
Code for semantic dual task for Perception Lab @ Carleton.

Files and their purposes:
- `sdt_word_lists.csv`: The four word lists in here are imported by `main.py`.
- `tape.json`: This dictionary maps participant id to the order of word lists and noises received by the corresponding participant. I generated this mapping randomly; in reality, this should be generated using counter-balancing.
- `integer_2_noise_order`: This dictionary maps integer index to order of four noises.
- `letter_2_word_list_order`: This dictionary maps integer index to order of four word lists.
- `instructions`: This dictionary maps event to messages that we would like to display to our participants.
- `main.py`: Run this script using PsycoPy. 
- `data`: Data will be saved here. First column: word index; second column: noun response; third column: response time. This need to be analyzed later by referencing `tape.json`.

TODOs:
- Add noise files
- Finish up instructions
