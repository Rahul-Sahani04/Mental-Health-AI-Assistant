# Mental Support Chatbot App

This Streamlit app implements a Mental Support Chatbot using the Google Generative AI model. The chatbot provides a listening ear and support for mental well-being, responding to user inputs with empathy and understanding.

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/Rahul-Sahani04/Mental-Health-AI-Assistant.git
    cd Mental-Health-AI-Assistant
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables by creating a `.env` file with the following content:

    ```dotenv
    GENAI_API_KEY=your_google_generative_ai_api_key
    ```

    Replace `your_google_generative_ai_api_key` with your actual Google Generative AI API key.

4. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

## Usage

1. Enter your messages in the text input field.

2. Click the "Send" button to interact with the chatbot.

3. The chatbot will respond with supportive messages related to mental health.

## Conversation History

The conversation history is loaded from the `conversation_history.json` file. You can customize the conversation or extend it as needed.

## Contributing

Feel free to contribute to the project by opening issues or pull requests. If you have any suggestions or improvements, we welcome your feedback!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
