inputUsername = document.querySelector('#username')
inputEmail = document.querySelector('#email')
message = document.querySelector('#message')
submitBtn = document.querySelector('#sign-up')
errors = []

inputUsername.addEventListener('keyup', (e) => {
  inputValue = e.target.value.toLowerCase()
  validate(inputValue, `validate/username/${inputValue}`, 'username')
})

inputEmail.addEventListener('keyup', (e) => {
  inputValue = e.target.value.toLowerCase()
  validate(inputValue, `validate/email/${inputValue}`, 'email')
})

const validate = (inputValue, url, type) => {
  if (inputValue.length > 0) {
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        message.classList.remove('alert-success')
        message.classList.remove('alert-danger')
        message.classList.remove('alert-warning')
        message.classList.remove('alert-info')

        if (data.error) {
          message.classList.add('alert-info')
          message.innerHTML = data.errorMessage
          if (!errors.includes(type)) {
            errors.push(type)
          }
        } else {
          if (data.available) {
            message.classList.add('alert-success')
            message.innerHTML = `<strong>${inputValue}</strong> is available`

            index = errors.indexOf(type)
            if (index > -1) {
              errors.splice(index, 1)
            }
          } else {
            message.classList.add('alert-danger')
            message.innerHTML = `<strong>${inputValue}</strong> is not available`

            if (!errors.includes(type)) {
              errors.push(type)
            }
          }
        }

        if (errors.length == 0) {
          submitBtn.removeAttribute('disabled')
        } else {
          submitBtn.setAttribute('disabled', true)
        }
      })
  }
}
