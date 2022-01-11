const $logInBtn = $('#logInBtn');
const $pwFindBtn = $('#pwFindBtn');
const $signUpBtn = $('#signUpBtn');
const $pwFindCheckBtn = $('#pwFindCheckBtn');

$logInBtn.click((e) => {
  e.preventDefault();
  let ID = $('#idInput').val();
  let PW = $('#pwInput').val();

  if(ID === '') { return alert('아이디를 적어주세요'); };
  if(PW === '') { return alert('비밀번호를 입력하세요.'); };

  $.ajax({
    type: "POST",
    url: "/api/user",
    data: { ID, PW },
    success: (res) => {
      if(res.token) {
        $.cookie('YouTuverse_token', res.token);

        alert('로그인 하였습니다.');
       return window.location.href = "/"
      }
      alert(res.msg);
    }
  });
});

$signUpBtn.click((e) => {
  e.preventDefault();
  window.location.href = "/signup";
});

$pwFindBtn.click((e) => {
  e.preventDefault();
  window.location.href = '/login/pw'
});

$pwFindCheckBtn.click((e) => {
  e.preventDefault();

  const user_id = $('#pwFindIdInput').val()
  const password = $('#newPwInput').val()
  if(user_id === '') { return alert('아이디를 입력하세요.'); };
  if(password === '') { return alert('변경할 비밀번호를 입력하세요.'); };

  $.ajax({
    type: 'POST',
    url: '/api/user/password',
    data: { user_id: user_id, password: password },
    success: (res) => {
      alert(res.msg);
      window.location.href = "/login"
    }
  })
})