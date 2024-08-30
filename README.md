# Diet Recommendation App

This project is a Flask-based web application that provides personalized diet recommendations based on user inputs such as age, weight, height, gender, activity level, and dietary goals. The app utilizes the FatSecret API to fetch food and recipe data, ensuring that the diet plans are both accurate and diverse.

## Purpose

The goal of this project is to create a program that recommends meals tailored to individuals' body types and preferences, especially for those starting a fitness journey.

## Development Timeline

- **Start Date**: 2024.08.28
- **End Date**: 2024.08.30

## AI Training by Sangmyung University

- **Idea Note Creation**
- **Presentation and Evaluation**

## Technology Stack

- **Ollama**: Python-based AI model for generating diet recommendations.
- **Front-end**: (Not yet decided)

## Project Architecture

### Page Functions

- **[Home Page]**
  - The UI is designed to collect personal information from users.
  - Users can immediately check their BMI score upon entering their data.
  - ![image](https://github.com/user-attachments/assets/1c7815c2-a512-4701-ac96-dace796b88b0)

- **[Results Page]**
  - Based on the user's personal information, the app recommends an optimized diet plan.
  - Users can receive alternative recommendations by specifying foods they like or dislike.
  - ![image](https://github.com/user-attachments/assets/98330f2e-15b2-4a36-bc5d-cf9643cd58dd )

## Key Features

1. **User Information Collection**: Collect personal data such as height, weight, goal, gender, and activity level, which is then input into Ollama AI.
2. **Diet Search**: Using the collected data, Ollama AI determines the appropriate diet for the user and provides recommendations.
3. **Diet Re-evaluation**: If the user is not satisfied with the initial diet plan, they can input their preferred or disliked foods to receive a new recommendation.

## Future Enhancements

1. **API Server Improvement**: Currently, the API is set to individual IPs. Future versions will allow multiple users to access the service without needing to configure their IPs by centralizing the API server.
2. **Alternative AI Models**: Explore other AI APIs to replace Ollama if its responses are slow or include unnecessary information.
3. **Muscle Mass and Body Fat Percentage**: Incorporate these metrics to provide more accurate diet recommendations.
4. **BMI Chart Enhancement**: Improve the BMI chart to allow the x-axis to move dynamically based on user input.

## Installation

### Prerequisites

Before you begin, ensure you have Python installed on your machine. You'll also need an API key from FatSecret.

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ttuurrnn/my-diet-app.git
    cd my-diet-app
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your environment variables:**

    Create a `.env` file in the project root and add your FatSecret API credentials:

    ```plaintext
    CLIENT_ID=your_fatsecret_client_id
    CLIENT_SECRET=your_fatsecret_client_secret
    ```

5. **Run the application:**

    ```bash
    python app.py
    ```

6. **Access the application:**

    Open your web browser and navigate to `http://localhost:5000`.

## Usage

1. **Input your details**: On the main page, enter your age, weight, height, gender, activity level, and dietary goal (e.g., weight loss, muscle gain).
2. **Get your diet plan**: Click "맞춤형 다이어트 식단 추천 받기" to generate a customized diet plan.
3. **Review your plan**: The app will display a diet plan with meals and recipes, along with a breakdown of calories and macronutrients.

## Project Structure

- **`app.py`**: The main Flask application file, containing all the routes and logic.
- **`templates/index.html`**: The main page where users input their information.
- **`templates/result.html`**: The results page displaying the recommended diet plan.
- **`requirements.txt`**: A list of all Python dependencies required to run the app.

## Technologies Used

- **Flask**: A lightweight web framework for Python used to build the application.
- **FatSecret API**: Used to retrieve food and recipe data for generating diet plans.
- **Tailwind CSS**: A utility-first CSS framework for styling the user interface.
- **Chart.js**: Used for visualizing BMI (Body Mass Index) on the front end.

## Future Enhancements

- **Enhanced Recipe Recommendations**: Improve the diversity of recommended recipes by integrating more advanced search criteria.
- **User Accounts**: Allow users to save their dietary plans and track their progress over time.
- **Multi-language Support**: Add support for multiple languages to cater to a broader audience.

## Acknowledgements

Special thanks to the FatSecret API team for providing a comprehensive API that made this project possible.
