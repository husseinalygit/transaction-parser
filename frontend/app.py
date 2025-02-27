import streamlit as st
import pandas as pd
from datetime import datetime
import src.config as config
from src.utils import append_to_csv, load_csv
from src.services import extract_ner, classify_transaction, chat_request
import time

st.title("Transaction Analysis System")

# Sidebar for initializing transaction history
with st.sidebar:
    st.header("Initialize Transaction History")
    uploaded_file = st.file_uploader("Upload Preprocessed Transactions", type=['csv'])
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            st.write(f"Found {len(df_upload)} transactions")
            if st.button("Initialize History"):
                # Save the uploaded file as the new transaction history
                df_upload.to_csv(f"{config.CSV_PATH}/{config.CSV_FILENAME}", index=False)
                st.success(f"Transaction history initialized with {len(df_upload)} records!")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# Main app content
# Display categories in expander
with st.expander("View Transaction Categories"):
    st.json(config.CATEGORIES)

# Input section
st.header("Transaction Analysis")
input_option = st.radio("Select Input Method", 
                       ["Single Message", "Multiple Messages"])

if input_option == "Multiple Messages":
    messages = st.text_area(
        "Enter multiple messages (one per line)", 
        height=200,
        help="Enter each SMS message on a new line"
    )
    
    if st.button("Process Messages"):
        if not messages.strip():
            st.error("Please enter at least one message.")
        else:
            message_list = [msg.strip() for msg in messages.split('\n') if msg.strip()]
            st.info(f"Processing {len(message_list)} messages...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            results_container = st.container()
            
            processed_results = []
            for idx, message in enumerate(message_list):
                status_text.text(f"Processing message {idx + 1} of {len(message_list)}...")
                progress_bar.progress((idx + 1) / len(message_list))
                
                # Process each message
                with st.spinner(f"Processing message {idx + 1}..."):
                    # Step 1: Extract entities using NER service
                    ner_result = extract_ner(message)
                    if ner_result:
                        # Step 2: Classify transaction using classification service
                        cls_result = classify_transaction(ner_result)
                        if cls_result:
                            # Combine results
                            final_record = {
                                "message": message,
                                **ner_result,
                                "Code": cls_result.get("Code"),
                                "Label": cls_result.get("Label"),
                                "Reason": cls_result.get("Reason"),
                                "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            processed_results.append(final_record)
                            # Store in CSV
                            append_to_csv(final_record, 
                                        filepath=config.CSV_PATH, 
                                        filename=config.CSV_FILENAME)
            
            # Display final results
            with results_container:
                st.success(f"Processed {len(processed_results)} messages successfully!")
                if processed_results:
                    st.subheader("Processing Results:")
                    df_results = pd.DataFrame(processed_results)
                    st.dataframe(df_results)

else:  # Single Message
    sms_message = st.text_area("Enter SMS message", height=150)
    
    if st.button("Process Transaction"):
        if sms_message.strip() == "":
            st.error("Please enter a valid message.")
        else:
            with st.spinner("Processing transaction..."):
                # Step 1: Extract entities using NER service
                ner_result = extract_ner(sms_message)
                if ner_result:
                    # Step 2: Classify transaction using classification service
                    cls_result = classify_transaction(ner_result)
                    if cls_result:
                        # Combine results
                        final_record = {
                            "message": sms_message,
                            **ner_result,
                            "Label": cls_result.get("Label"),
                            "Code": cls_result.get("Code"),
                            "Reason": cls_result.get("Reason"),
                            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        # Display results
                        st.subheader("Processing Results:")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("Extracted Entities:")
                            st.json(ner_result)
                        with col2:
                            st.write("Classification:")
                            st.json({
                                "Label": final_record["Label"],
                                "Code": final_record["Code"],
                                "Reason": final_record["Reason"]
                            })
                        
                        # Store in CSV
                        append_to_csv(final_record, 
                                    filepath=config.CSV_PATH, 
                                    filename=config.CSV_FILENAME)
                        st.success("Transaction processed and saved successfully!")

# Display historical data
st.header("Transaction History")

# Create two columns: one for the refresh button and one for any additional controls
col1, col2 = st.columns([1, 5])
with col1:
    refresh = st.button("🔄 Refresh")

# Load and display data (happens by default)
df = load_csv(filepath=config.CSV_PATH, filename=config.CSV_FILENAME)
if df.empty:
    st.info("No transactions recorded yet.")
else:
    st.dataframe(df, use_container_width=True)
    st.write(f"Total transactions: {len(df)}")

# Force a rerun if refresh button is clicked
if refresh:
    st.rerun()

# Add Chat Interface at the bottom
st.header("Chat with Your Transaction Data")
st.write("Ask questions about your transactions. For example:")
st.info("""
- What was my highest expense in Dec 2024 ?
- what month had the highest spending?
- What's my average spending?
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your transactions"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_request(prompt)
            print(response)
            if response:
                if "model_response" in response:
                    st.markdown(response["model_response"])
                if "processed_response" in response: 
                    # show the processed response in a box different from the model response
                    st.markdown (f"**Processed Response:**\n```\n{response['processed_response']}\n```")

                st.session_state.messages.append({"role": "assistant", "content": response.get("processed_response", response["model_response"])})
            else:
                st.error("Failed to get response from the chat service")

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()
