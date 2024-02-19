function togglePasswordVisibility() {
    var passwordInput = document.getElementById("passwordInput");
    var toggleIcon = document.querySelector(".toggle-password");

    if (passwordInput.type === "password") {
passwordInput.type = "text";
      toggleIcon.textContent = "✕"; // 眼のアイコンに表示を切り替える絵文字
    } else {
passwordInput.type = "password";
      toggleIcon.textContent = "👁"; // 目のアイコンに表示を切り替える絵文字
    }
}
