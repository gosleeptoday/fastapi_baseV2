function register() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const firstName = document.getElementById('firstName').value;
    const secondName = document.getElementById('secondName').value;
    const surName = document.getElementById('surName').value;
    const user_id = 0;
  
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:8000/user/signup', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
  
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          console.log('Registration successful', xhr.responseText);
          // Здесь можно выполнить дополнительные действия после успешной регистрации
        } else {
          console.error('Registration failed', xhr.responseText);
          // Здесь можно обработать ошибку регистрации
        }
      }
    };
  
    const data = JSON.stringify({
      user: {
        email: email,
        password: password,
      },
      userinf: {
        FirstName: firstName,
        SecondName: secondName,
        SurName: surName,
        user_id: user_id
      },
    });
  
    xhr.send(data);
  }
  