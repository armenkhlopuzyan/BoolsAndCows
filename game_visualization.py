from secret_data_generator import SecretNumbers, SecretWord
import streamlit as st
import base64


def play_game():
    st.set_page_config(layout='wide')

    background = """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #071552, #4A1576);
        color: white; /* Optional: Ensure text is readable */
    }
    </style>
    """
    st.markdown(background, unsafe_allow_html=True)

    # Center the text horizontally (using CSS)
    st.markdown("<div style='text-align: center; font-size: 24px; color: yellow;'>Guess the hidden code!</div>",
                unsafe_allow_html=True)
    image_path = "BC_logo_nb.png"
    # Read the image file and encode it in base64 (converting to a base64 string)
    with open(image_path, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode()

    # Center the image (using HTML and CSS)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{encoded_image}" alt="Centered Image" width="250">
        </div>
        """,
        unsafe_allow_html=True
    )

    def create_option_button(style, label, num_generator, duplicate):
        st.markdown(style, unsafe_allow_html=True)
        if st.button(label):
            st.session_state.hidden_code = num_generator()
            print("===KHA_DBG===  hidden_code:", st.session_state.hidden_code)
            st.session_state.duplicate_allowed = duplicate
            st.rerun()

    # Initializing session state
    if "hidden_code" not in st.session_state:
        st.write("")
        st.write("")
        #st.markdown("<div style='text-align: center; font-size: 48px;'> 🔑 </div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 18px; color: #66FF99;'>Select an option to start the game!</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 24px; color: white;'>Options</div>", unsafe_allow_html=True)
        button_style = """
                    <style>
                    .stButton button {
                        background-color: #4cabcd;
                        color: white; 
                        width: 120px !important;   /* Set button width */         
                        font-size: 24px;           /* No effect */ 
                        cursor: pointer;           /* Pointer cursor on hover */
                        display: block !important; /* Prevent vertical shift */
                    }
                    /* Adding hover effect */
                    .stButton button:hover {
                        background-color: #45a049; /* Dark green hover */
                        color: yellow; 
                        border: 4px solid yellow;   
                        border-radius: 8px;        /* Rounded corners */
                    }
                    </style>
                    """
        st.markdown(button_style, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([4, 1.5, 1.5, 4])
        with col2:
            st.markdown("<div style='text-align: center; font-size: 24px; color: white;'><I>Guess Number with ..</I></div>",
                        unsafe_allow_html=True)
        with col3:
            st.markdown("<div style='text-align: center; font-size: 24px; color: white;'><I>Guess Word with ..</I></div>",
                        unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns([5.3, 0.5, 1.4, 0.9, 5.4])
        with col2:
            for i in range(3, 6):
                num_gen = SecretNumbers(i).generate_numbers
                create_option_button(button_style, f"{i} digits", num_gen, False)
        with col4:
            for i in range(5, 8):
                word_gen = SecretWord(i).generate_word
                create_option_button(button_style, f"{i} letters", word_gen, True)

    if "hidden_code" in st.session_state:
        if "attempts" not in st.session_state:
            st.session_state.attempts = []
        if "bulls_cows_stat" not in st.session_state:
            st.session_state.bulls_cows_stat = []
        if "revealed" not in st.session_state:
            st.session_state.revealed = ["?" for _ in range(len(st.session_state.hidden_code))]
        if "after_1st_attempt" not in st.session_state:
            st.session_state.after_1st_attempt = False
        if "invalid_input" not in st.session_state:
            st.session_state.invalid_input = False, ""
        if "give_up" not in st.session_state:
            st.session_state.give_up = False
        if st.session_state.give_up:
            st.session_state.revealed = st.session_state.hidden_code

        n = len(st.session_state.hidden_code)

        st.markdown(
            """
            <div style="text-align: center; font-size: 24px; color: #dbdd90;">
                <p>Use mouse or Tab to enter your guess in each field.<br>
                <span style="color: #66FF99;">Bulls: correct code, correct position. <span style="color: white;">/  
                <span style="color: orange;">Cows: correct code, wrong position.</p>      
            </div>
            """,
            unsafe_allow_html=True
        )

        # Function to check input and update revealed cells
        def accept_input(user_input_data, hidden_code_data):
            #print("===KHA=== user_input:", user_input_data)
            #print("===KHA===   hid_code:", hidden_code_data)
            current_attempt = []
            bulls, cows = 0, 0
            #print("n:", n)
            for j in range(n):
                current_attempt.append(user_input_data[j])
                if user_input_data[j] == hidden_code_data[j]:
                    bulls += 1
                elif user_input_data[j] in hidden_code_data:
                    cows += 1
            # Check if all numbers are revealed
            if current_attempt == hidden_code_data:
                st.session_state.revealed = current_attempt
                # print(st.session_state.revealed)
            st.session_state.attempts.append(current_attempt)
            st.session_state.bulls_cows_stat.append([bulls, cows])

        st.markdown(
            """
            <style>
            .cell-container {display: flex; justify-content: center; align-items: center; gap: 3px; margin-bottom: 3px;}
            .cell {
                width: 50px;
                height: 50px;
                font-size: 24px;
                text-align: center;
                line-height: 50px;
                border: 4px solid #4CAF50;
                border-radius: 5px;
                background-color:  #f1f1f1;
                color: black;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Render the cells dynamically
        code = "Word" if st.session_state.duplicate_allowed else "Number"
        st.markdown(f"<div style='text-align: center; font-size: 24px; color: yellow'>Hidden {code}</div>",
                    unsafe_allow_html=True)
        cells_html = "<div class='cell-container' style='display: flex;'>"
        for value in st.session_state.revealed:
            cells_html += f"""
                <div class='cell'
                 style='background-color: yellow; color: green; display: flex; align-items: center; justify-content: center;'>
                 <b>{value}</b></div>"""
        cells_html += "</div>"
        st.markdown(cells_html, unsafe_allow_html=True)

        if st.session_state.after_1st_attempt:
            # Displaying all user input attempts
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                st.write("")
                st.markdown("<div style='text-align: center; font-size: 24px; color: white'>Attempts</div>",
                            unsafe_allow_html=True)
                if len(st.session_state.attempts) != 0:
                    for attempt in st.session_state.attempts:
                        cells_html = "<div class='cell-container' style='display: flex;'>"
                        for value in attempt:
                            cells_html += f"<div class='cell' style='display: flex; align-items: center; justify-content: center;'>{value}</div>"  # Hidden cell
                        cells_html += "</div>"
                        st.markdown(cells_html, unsafe_allow_html=True)
            with col3:
                st.write("")
                bulls_cows = "<div style='text-align: left; font-size: 22px; color: #66FF99'>Bulls"
                bulls_cows += "<span style='color: #21136B'>-<span style='color: orange'>Cows</div>"
                bulls_cows += "</div>"
                st.markdown(bulls_cows, unsafe_allow_html=True)
                if len(st.session_state.bulls_cows_stat) != 0:
                    for stat in st.session_state.bulls_cows_stat:
                        cells_html = "<div class='cell-container'; style='text-align: left display: flex; justify-content: flex-start;'>"
                        for i, value in enumerate(stat):
                            color = '#66FF99' if i == 0 else 'orange'
                            cells_html += f"<div class='cell'; style='border: none; background-color: {color}; align-items: center;'>{value}</div>"
                        cells_html += "</div>"
                        st.markdown(cells_html, unsafe_allow_html=True)

        button_style = """
                    <style>
                    .stButton button {
                        background-color: #4cabcd;
                        color: white;     
                        width: 120px !important;    /* Set button width */         
                        font-size: 24px;           
                        cursor: pointer;           /* Pointer cursor on hover */
                        display: block !important;     /* Prevent vertical shift */
                    }
                    /* Adding hover effect */
                    .stButton button:hover {
                        background-color: #45a049; /* Dark green hover */
                        color: yellow; 
                        border: 4px solid yellow;   
                        border-radius: 8px;        /* Rounded corners */
                    }
                    </style>
                    """

        def create_play_again_button(style: str, label: str):
            col_1, col_2 = st.columns([11, 13])
            with col_2:
                st.markdown(style, unsafe_allow_html=True)
                if st.button(label):
                    st.session_state.clear()  # Clears all session state variables
                    st.rerun()

        if not st.session_state.give_up:
            if st.session_state.revealed[0] == '?':
                if st.session_state.after_1st_attempt:
                    st.markdown("<div style='text-align: center; font-size: 24px; color: #dbdd90;'>Try Again</div>",
                                unsafe_allow_html=True)
                if st.session_state.invalid_input[0]:
                    st.markdown(
                        f"""<div style='text-align: center; font-size: 24px; color: red;'><b>Please enter VALID data 
                            {st.session_state.invalid_input[1]}.</b></div>""",
                        unsafe_allow_html=True)

            if st.session_state.revealed[0] == '?':
                st.markdown(
                    """
                    <style>
                        label { display: none !important;}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("<div style='text-align: center; font-size: 24px; color: yellow;'>Enter Your Guess</div>",
                            unsafe_allow_html=True)
                col1, col2, col3, col4, col5, col6 = st.columns([5, 1, n * 0.5, 1, 4, 1])
                with col3:
                    st.write("")
                    if st.session_state.revealed[0] == '?':
                        # Input boxes for the current attempt
                        cols = st.columns(n)
                        user_input = []
                        for i, col in enumerate(cols):
                            with col:
                                inp = st.text_input("hidden_code", max_chars=1, key=f"input_{len(st.session_state.attempts)}_{i}")
                                if inp != '': user_input.append(inp)
                                # user_input.append(
                                #     st.text_input("hidden_code", max_chars=1,
                                #                   key=f"input_{len(st.session_state.attempts)}_{i}"))
                with col5:
                    # Add custom CSS to style the button
                    st.markdown(button_style, unsafe_allow_html=True)
                    if True:
                        col01, col02, col03 = st.columns([1, 1, 1])
                        with col01:
                            # Submit button to process the user input
                            if st.button("Submit"):
                                st.session_state.after_1st_attempt = True
                                if len(user_input) != len(st.session_state.hidden_code):
                                    st.session_state.invalid_input = True, "(incomplete input)"
                                    st.rerun()
                                if user_input[0] == '0':
                                    st.session_state.invalid_input = True, "('0' in first position)"
                                    st.rerun()
                                if st.session_state.duplicate_allowed:
                                    if not all(len(x) == 1 and x.isalpha() for x in user_input):
                                        st.session_state.invalid_input = True, "(non-alphabetic input)"
                                        st.rerun()
                                else:
                                    if not all(len(x) == 1 and x.isdigit() for x in user_input):
                                        st.session_state.invalid_input = True, "(non-numeric input)"
                                        st.rerun()
                                    if len(set(user_input)) != len(user_input):
                                        st.session_state.invalid_input = True, "(duplicates)"
                                        st.rerun()
                                st.session_state.invalid_input = False, ""
                                accept_input(user_input, st.session_state.hidden_code)
                                st.rerun()
                        with col02:
                            if st.button("New Game"):
                                st.session_state.clear()  # Clears all session state variables
                                st.rerun()
                        with col03:
                            if st.button("Give Up"):
                                st.session_state.give_up = True
                                st.rerun()
            else:
                st.markdown(f"""<div style='text-align: center; font-size: 42px; color: #66FF99;'>
                                <b>Congratulations!</b></div>""", unsafe_allow_html=True)
                st.markdown(f"""<div style='text-align: center; font-size: 42px; color: yellow;'>
                                You have guessed the hidden code correctly!</div>""", unsafe_allow_html=True)
                create_play_again_button(button_style, "Play Again")
        else:
            st.markdown(f"""<div style='text-align: center; font-size: 42px; color: red;'>
                            <b>Never Give Up!</b></div>""",
                        unsafe_allow_html=True)
            create_play_again_button(button_style, "Play Again")


if __name__ == "__main__":
    play_game()

















