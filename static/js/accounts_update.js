  // 모달창 열기
  function openNicknameModal() {
    var nicknameModal = document.getElementById('nicknameModal');
    nicknameModal.style.display = 'block';
  }
  
  // 모달창 닫기
  function closeNicknameModal() {
    var nicknameModal = document.getElementById('nicknameModal');
    nicknameModal.style.display = 'none';
  }
  
  // 닉네임이 설정되어 있는지 확인하는 함수
  function userNicknameExists() {
    var nicknameModal = document.getElementById('nicknameModal');
    if (!nicknameModal) {
      return false;
    }
    var userNickname = nicknameModal.dataset.userNickname;
  
    if (userNickname === "None") {
      return false; // 닉네임이 비어 있거나 null인 경우
    } else {
      return true; // 닉네임이 설정되어 있는 경우
    }
  }
  
  window.addEventListener('DOMContentLoaded', function() {
    // 닉네임이 설정되어 있는지 확인
    if (!userNicknameExists()) {
      openNicknameModal();
    }
  
    var nicknameSubmitBtn = document.getElementById('nicknameSubmitBtn');
  
    // 모달창 확인 버튼 클릭 이벤트 처리
    nicknameSubmitBtn.addEventListener('click', function(event) {
      event.preventDefault(); // 기본 동작 방지
      // 모달창 닫기
      closeNicknameModal();
    });
  
    // 모달창 외의 영역 클릭 시 모달창 닫기
    window.addEventListener('click', function(event) {
      var nicknameModal = document.getElementById('nicknameModal');
      if (event.target === nicknameModal) {
        closeNicknameModal();
      }
    });
  });