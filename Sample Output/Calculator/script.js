// script.js – Calculator interactive logic
// This script runs with `defer`, so the DOM is already loaded.

(() => {
  // ---------------------------------------------------------------------------
  // Global element references
  // ---------------------------------------------------------------------------
  const display = document.getElementById('display');
  const buttons = document.querySelectorAll('#calculator button');

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------
  let currentExpression = '';

  // ---------------------------------------------------------------------------
  // Helper functions
  // ---------------------------------------------------------------------------
  function updateDisplay() {
    display.value = currentExpression || '0';
  }

  function isOperator(ch) {
    return ['+', '-', '*', '/', '×', '÷'].includes(ch);
  }

  function appendCharacter(char) {
    // Allow digits
    if (/^[0-9]$/.test(char)) {
      currentExpression += char;
      return;
    }

    // Decimal point – only one per number segment
    if (char === '.') {
      // Find the part after the last operator
      const parts = currentExpression.split(/[+\-*/×÷]/);
      const lastPart = parts[parts.length - 1];
      if (!lastPart.includes('.')) {
        // If the expression is empty, prepend a leading zero
        if (lastPart === '') {
          currentExpression += '0.';
        } else {
          currentExpression += '.';
        }
      }
      return;
    }

    // Operators – prevent two consecutive operators (except leading '-')
    if (isOperator(char)) {
      if (currentExpression === '' && char !== '-') {
        // Do not allow starting expression with an operator other than '-'
        return;
      }
      const lastChar = currentExpression.slice(-1);
      if (isOperator(lastChar)) {
        // Replace the previous operator with the new one
        currentExpression = currentExpression.slice(0, -1) + char;
      } else {
        currentExpression += char;
      }
      return;
    }
    // Any other characters are ignored
  }

  function clearDisplay() {
    currentExpression = '';
    updateDisplay();
  }

  function backspace() {
    currentExpression = currentExpression.slice(0, -1);
    updateDisplay();
  }

  function evaluateExpression() {
    if (!currentExpression) {
      return '0';
    }
    // Normalise symbols
    let expr = currentExpression.replace(/÷/g, '/').replace(/×/g, '*');
    // Guard against malicious code – only allow numbers, operators and decimal points
    if (!/^[0-9+\-*/.()\s]+$/.test(expr)) {
      throw new Error('Invalid characters');
    }
    let result;
    try {
      // Using Function constructor instead of eval for a tiny bit more safety
      result = Function('return ' + expr)();
    } catch (e) {
      throw new Error('Syntax error');
    }
    // Detect division by zero (result will be Infinity or -Infinity)
    if (result === Infinity || result === -Infinity) {
      throw new Error('Division by zero');
    }
    // Handle NaN (e.g., empty evaluation)
    if (Number.isNaN(result)) {
      throw new Error('Invalid expression');
    }
    // Round to avoid floating‑point artefacts
    result = Number(result.toFixed(10));
    return result.toString();
  }

  // ---------------------------------------------------------------------------
  // UI handling
  // ---------------------------------------------------------------------------
  function handleInput(value) {
    try {
      if (value === 'C') {
        clearDisplay();
      } else if (value === '←') {
        backspace();
      } else if (value === '=') {
        const result = evaluateExpression();
        currentExpression = result;
        updateDisplay();
      } else {
        appendCharacter(value);
        updateDisplay();
      }
    } catch (err) {
      // Show temporary error message
      display.value = 'Error';
      setTimeout(() => {
        clearDisplay();
      }, 1500);
    }
  }

  // Attach click listeners to all calculator buttons
  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      const value = button.dataset.value;
      handleInput(value);
    });
  });

  // Keyboard support – map keys to the same values used by buttons
  const keyMap = {
    Escape: 'C',
    Backspace: '←',
    Enter: '=',
    '=': '=',
    '+': '+',
    '-': '-',
    '*': '*',
    '/': '/',
    '.': '.',
    ',': '.', // some keyboards use comma for decimal
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
  };

  document.addEventListener('keydown', (e) => {
    const mapped = keyMap[e.key];
    if (mapped) {
      e.preventDefault();
      handleInput(mapped);
    }
  });

  // Initialise display
  updateDisplay();

  // ---------------------------------------------------------------------------
  // Testing hooks – expose functions on the global window object
  // ---------------------------------------------------------------------------
  window.calculator = {
    appendCharacter,
    clearDisplay,
    backspace,
    evaluateExpression,
    getExpression: () => currentExpression,
  };
})();
