# Financial assitant project for bank of baroda hackathon
A Gen-AI powered financial assistant bot that will help the consumers who require assistance , whether it is about navigating the banks website or highly specific queries regarding policies , whose answers may not be easily inferable from the FAQs , especially for first time users or senior citizens and so on . Our bot also helps users get financial advice given their current assets by providing users with options about which policies might be right for them , how to manage their finances in a way that it accomplishes their objectives etc .

Methodology:
The approach to building this financial assistant involves integrating a React-based frontend with a Flask backend that utilizes the Azure OpenAI platform for natural language processing. The primary goals are to ensure a responsive and user-friendly interface, seamless backend communication, and scalable architecture to handle increasing load efficiently.
Frontend Development:
React: Chosen for its component-based architecture, allowing for modular development and easy maintenance.
CSS: Used for responsive design to ensure the chatbot works well on different screen sizes.
Axios: Used for making HTTP requests to the backend, providing a clean and simple way to interact with APIs.
Backend Development:
Flask: A lightweight and easy-to-setup web framework for handling HTTP requests and serving as the bridge between the frontend and Azure OpenAI.
Azure OpenAI: Provides the necessary NLP capabilities to process user inputs and generate appropriate responses.
Scalability:
Load Balancing: Using a load balancer to distribute incoming requests across multiple instances of the backend server.
Horizontal Scaling: Adding more instances of the backend service as the load increases.
Caching: Implementing caching mechanisms to store frequently accessed data and reduce the load on the server.

flowchart and working of the model:

<img width="1136" alt="Screenshot 2024-08-01 at 8 45 12 PM" src="https://github.com/user-attachments/assets/91dc3966-5f5c-478d-a2c7-a7e73fdd8122">

User Interaction:

The user sends a message through the User Interface.

<img width="506" alt="Screenshot 2024-08-01 at 8 46 39 PM" src="https://github.com/user-attachments/assets/5ef723b1-8272-4795-a7e8-7660d895ad74">

React Frontend:
deployed: https://bob-assist.vercel.app/
The Chat component handles the user message.
The sendMessage() function is called, which:
Adds the user's message to the local messages state.
Sends the message to the backend via an Axios POST request to /api/message.

Flask API (Backend Server):
The Flask route /api/message receives the message.
The route handler calls the handle_message() function with the user's message.
Processing the Message:

The handle_message() function:
Creates a thread in the Azure OpenAI service.
Adds the user's message to the thread.
Runs the thread and waits for a response.
Simultaneously, the Azure OpenAI service processes the message and generates a response.

Azure OpenAI Service:
The service processes the user's message.
Returns the generated bot response.

Return Response:
The handle_message() function receives the bot response.
The Flask API sends this response back to the React frontend via Axios.

React Frontend (Continued):
The frontend receives the bot's response.
Updates the messages state with the new bot message.

Chat Component:
The Chat component re-renders to display the user and bot messages.
This flowchart and explanation provide a comprehensive overview of the application's working, ensuring clarity in understanding each step and the concurrent processes involved.
