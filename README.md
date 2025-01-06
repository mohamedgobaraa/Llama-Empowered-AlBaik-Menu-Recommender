# Llama-Empowered AlBaik Menu Recommender

This project implements a Flask-based web application for recommending menu items from AlBaik, a popular Saudi restaurant chain. The application uses AI-powered suggestions based on user preferences, leveraging the Llama model for natural language understanding and recommendation generation.

## Features
- **Interactive User Interface**: Input price range, calorie preferences, meal categories, and more.
- **AI Recommendations**: Generate customized menu suggestions using the Llama model.
- **Dynamic Filtering**: Narrow down menu items by price, calories, and categories.
- **Real-Time Suggestions**: Responds dynamically to user inputs and updates recommendations accordingly.

## Prerequisites
1. **Python 3.7 or higher**
2. **Flask Framework**
3. **Required Libraries**: Install dependencies via `pip`:

   ```bash
   pip install flask pandas ollama
   ```
4. **CSV File**: The `AlBaik.csv` file must contain menu data with the following columns:
   - `Item Name`
   - `Price`
   - `Calories`
   - `Description`
   - `Category`
   - `Image Path`

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/llama-albaik-menu-recommender.git
   cd llama-albaik-menu-recommender
   ```

2. **Prepare the Data**:
   - Ensure the `AlBaik.csv` file is present in the project directory with the required columns.

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## API Endpoints

### `GET /`
- **Description**: Renders the main page with filters for price, calories, and category.

### `POST /get_suggestions`
- **Description**: Accepts user preferences and returns AI-generated menu recommendations.
- **Request Body**:
  ```json
  {
    "min_price": 10,
    "max_price": 50,
    "min_calories": 200,
    "max_calories": 1000,
    "category": ["Chicken", "Seafood"],
    "meal_time": "Lunch",
    "sides": "Yes",
    "beverages": "Yes",
    "additional_sides": ["Fries"],
    "additional_beverages": ["Pepsi"]
  }
  ```
- **Response Example**:
  ```json
  {
    "suggestions": [
      {
        "Item Name": "وجبة دجاج مسحب – ١٠ قطع",
        "Price": 21,
        "Calories": 1262,
        "Description": "قطع دجاج مقرمشة...",
        "Image Path": "382f6d5233ba450b0d8fe9f1c7e67e32.jpg"
      }
    ]
  }
  ```

## File Structure
```
.
├── app.py                # Main application file
├── templates/
│   └── index.html        # HTML template for the main page
├── AlBaik.csv            # Menu data file
├── static/
│   └── css/
│       └── styles.css
├── images/               # Folder for menu item images
├── README.md             # Project documentation
```

## Llama Model Integration
This project utilizes the **Ollama** library to interact with the Llama model for generating menu recommendations. Ensure the library is correctly installed and the Llama model (`llama3.3`) is available locally.

## Customization
- **Add New Menu Items**: Update the `AlBaik.csv` file with new rows.
- **Modify Preferences**: Adjust the prompt in `app.py` to change how the AI responds to user inputs.

## Logging
The application logs AI responses and errors for debugging purposes. Logs can be reviewed in the console output.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
