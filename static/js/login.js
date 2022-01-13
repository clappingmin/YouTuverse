const $logInBtn = $('#logInBtn');
const $logoutBtn = $('#logoutBtn');
const $pwFindBtn = $('#pwFindBtn');
const $signUpBtn = $('#signUpBtn');
const $pwFindCheckBtn = $('#pwFindCheckBtn');

function logIn() {
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
};

function logOut() {
  $.ajax({
    type: 'GET',
    url: '/api/user/logout',
    data: {},
    success: (res) => {
      if(res.msg === 'success') {
        const YouTuverse_token = $.cookie('YouTuverse_token')
        $.removeCookie('YouTuverse_token', YouTuverse_token)
        window.location.href = '/'
      }
    },
    error: (error) => {
      alert('로그아웃에 실패하였습니다: ', error)
      window.location.href = '/'
    }
  });
};

function findPassword() {
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
  });
};

$logInBtn.click((e) => {
  e.preventDefault();
  logIn();
});

$signUpBtn.click((e) => {
  e.preventDefault();
  window.location.href = "/signup";
});

$pwFindBtn.click((e) => {
  e.preventDefault();
  window.location.href = '/login/pw'
});

$logoutBtn.click((e) => {
  e.preventDefault();
  logOut();
})





// 로그인
$('#pwInput').on('keyup', (e) => {
  e.preventDefault();
  console.log('로그인');
  if(window.event.keyCode === 13) { logIn(); };
});

// 비밀번호 찾기
$pwFindCheckBtn.click((e) => {
  e.preventDefault();
  findPassword();
});

$('#newPwInput').on('keyup', (e) => {
  e.preventDefault();
  console.log('비번 찾기');
  if(window.event.keycode === 13) { findPassword(); };
})