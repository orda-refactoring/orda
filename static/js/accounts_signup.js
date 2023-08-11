let usernameValidationPassed = false;

function checkUsername() {
  const username = document.getElementById('id_username').querySelector('input').value;       
  if (username) {
    const formData = new FormData();
    formData.append('username', username);
    const checkCsrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    axios({
      method: 'POST',
      url: '/accounts/signup/check_username/',
      headers: {
        'Content-Type': 'multipart/form-data',
        'X-CSRFToken': checkCsrftoken,
      },
      data: formData,
    })
    .then((response) => {
      const data = response.data;
      const validationMsg = document.getElementById('username-validation-msg');
      if (data.exists) {
        validationMsg.textContent = '●  이미 사용 중인 아이디입니다.';
        validationMsg.style = 'color:var(--red-color); margin-left: 10px; margin-top: 8px;';
        usernameValidationPassed = false;
      } else {
        validationMsg.textContent = '●  가능한 아이디입니다.';
        validationMsg.style = 'color:rgb(101, 101, 254); margin-left: 10px; margin-top: 8px;';
        usernameValidationPassed = true;
        // 필요한 경우 다른 input 활성화 등 추가 작업 수행
      }
      updateSubmitButtonState(); // 중복검사 결과에 따라 버튼 상태 업데이트 호출
    })
    .catch((error) => {
      console.error('Error:', error);
      usernameValidationPassed = false;
      updateSubmitButtonState(); // 버튼 상태 업데이트 호출
    });
  }
}

function updateSubmitButtonState() {
  const submitBtn = document.getElementById('submit-btn');
  submitBtn.disabled = !usernameValidationPassed; // 중복검사 통과하지 않으면 버튼 비활성화

  // 버튼의 상태에 따라 CSS 클래스를 추가하거나 제거
  if (submitBtn.disabled) {
    submitBtn.classList.add('disabled');
  } else {
    submitBtn.classList.remove('disabled');
  }
}
    

// 버튼 클릭 시 중복 검사 수행
document.getElementById('username-check-btn').addEventListener('click', checkUsername);

// 입력란에 글자를 입력할 때마다 중복 검사 수행 (옵션)
// document.getElementById('id_username').addEventListener('input', checkUsername);
