# SimpleCalculator

## Project Overview
SimpleCalculator is a lightweight, web‑based calculator that runs entirely in the browser. It provides basic arithmetic operations, a clean responsive UI, and keyboard support, making it handy for quick calculations on both desktop and mobile devices.

## Tech Stack
- **HTML** – Structure of the calculator interface.
- **CSS** – Styling, responsive layout, and theming via custom properties.
- **JavaScript** – Core calculation logic, display updates, and error handling (implemented in `script.js`).

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone <repository‑url>
   cd <repository‑directory>
   ```
2. **Open the application**
   - Simply open `index.html` in any modern web browser (Chrome, Firefox, Edge, Safari). No build step or server is required.

## Usage Guide
### Button Layout
- **Digits (0‑9)** – Click or press the corresponding number keys.
- **Operations** – `+` (addition), `-` (subtraction), `*` (multiplication), `/` (division).
- **Equals** – `=` button or **Enter** key.
- **Clear** – `C` button or **Esc** key (resets the entire expression).
- **Delete** – `←` button or **Backspace** key (removes the last character).
- **Decimal** – `.` button or `.` key.

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| 0‑9 | Insert digit |
| `+ - * /` | Insert operator |
| `Enter` | Evaluate (equals) |
| `Backspace` | Delete last character |
| `Esc` | Clear all |
| `.` | Decimal point |

### Error Messages
- **Division by zero** – Displays `Error: Division by zero` and prevents the operation.
- **Invalid expression** – If the expression cannot be parsed (e.g., two operators in a row), the display shows `Error: Invalid expression`.

## Responsive Design
The calculator UI is built with flexible CSS grid and media queries. On narrow screens (phones), buttons stack and scale to remain comfortably tappable, ensuring a smooth experience across devices.

## Development Notes
- **Core Logic** – Located in `script.js`. It parses the current expression, evaluates it using JavaScript's `Function` constructor, and updates the display element.
- **Display Updates** – The `updateDisplay()` function reflects the current expression or result in the `<div id="display">` element.
- **Error Handling** – Errors are caught in a `try/catch` block; the caught message is shown on the display and the internal state is reset to allow further input.
- **Theming** – `style.css` defines CSS custom properties (e.g., `--bg-color`, `--button-bg`) at the `:root` level. Changing these values updates the whole look without touching the markup or JavaScript.

## Contribution
Contributions are welcome! Follow these simple steps:
1. Fork the repository.
2. Create a new branch for your feature or bug‑fix.
3. Make changes, ensuring the existing functionality is not broken.
4. Test the calculator in a browser (desktop and mobile view).
5. Submit a pull request with a clear description of what was added or fixed.

### Guidelines
- Keep the UI simple and accessible.
- Avoid adding heavy dependencies; the project should stay lightweight.
- Write clear commit messages.
- If you add new functionality, update this README accordingly.

## License
This project is licensed under the MIT License – see the `LICENSE` file for details.
