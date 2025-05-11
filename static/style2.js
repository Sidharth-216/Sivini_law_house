document.addEventListener("DOMContentLoaded", () => {
    const registerButton = document.querySelector(".register-btn");
  
    registerButton.addEventListener("mouseover", () => {
      registerButton.style.transform = "translateY(-3px)";
    });
  
    registerButton.addEventListener("mouseout", () => {
      registerButton.style.transform = "translateY(0)";
    });
  
    const inputs = document.querySelectorAll("input[type='text'], input[type='email'], input[type='password']");
    inputs.forEach((input) => {
      input.addEventListener("focus", () => {
        input.style.backgroundColor = "rgba(255, 255, 255, 1)";
      });
  
      input.addEventListener("blur", () => {
        input.style.backgroundColor = "rgba(255, 255, 255, 0.8)";
      });
    });
  });
  