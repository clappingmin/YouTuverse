const $signUpBtn = $('#signUpBtn');

function signUp() {
  let ID = $('#idInput').val();
  let NICKNAME = $('#nicknameInput').val();
  let PW = $('#pwInput').val();
  let PW_CHECK = $('#pwCheckInput').val();

  const IDregExp = /^[A-Za-z0-9]{4,12}$/;

  if(ID === '') { return alert('아이디를 적어주세요.'); };
  if(!IDregExp.test(ID)) { return alert('아이디는 영문 혹은 숫자로, 4~12글자만 가능합니다. :D'); };
  if(NICKNAME === '') { return alert('닉네임을 적어주세요.'); };
  if(PW === '') { return alert('비밀번호를 입력하세요.'); };
  if(PW !== PW_CHECK) { return alert('비밀번호가 일치하지 않습니다.'); };
    
  $.ajax({
    type: "POST",
    url: "/api/user/new",
    data: { ID, NICKNAME, PW },
    success: (res) => {
      alert(res.msg)
      if(res.result === 'success') { window.location.href="/login" }
    }
  });
}

$signUpBtn.click((e) => {
  e.preventDefault();
  signUp();
});

$pwCheckInput.on('keyup', (e) => {
  e.preventDefault();
  signUp();
});