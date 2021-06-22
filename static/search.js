// SEARCH FUNCTIONALITY
searchInput = document.querySelector('#search-input')
results = document.querySelector('#results')
loader_container = document.querySelector('#loader-container')

searchInput.addEventListener('keyup', (e) => {
  searchValue = e.target.value

  if (searchValue.length > 0) {
    loader_container.removeAttribute('hidden')

    var absolute = function (rel) {
      var link = document.createElement('a')
      link.href = rel
      return link.protocol + '//' + link.host + link.pathname
    }

    domain = window.location.href
    absURL = absolute(`/articles/search-async/${searchValue}`)

    getData(absURL, (data) => {
      div = document.createElement('div')

      div.classList.add('row')

      html = makeHtml(data)
      div.innerHTML = html

      loader_container.setAttribute('hidden', true)
      results.innerHTML = ''
      results.append(div)
    })
  }
})

function getData(absURL, callback) {
  fetch(absURL)
    .then((response) => response.json())
    .then((data) => {
      callback(data)
    })
}

function makeHtml(data) {
  let html = `<h1 class="text-center text-success mt-2 mb-5">Searched Articles for <span class='text-capitalize'> "${searchValue} </span>"</h1>`

  if (data.length > 0) {
    data.forEach((articleModel) => {
      article = articleModel.fields
      title = article.title
      cover_image = article.cover_image
      modifiedAt = article.modifiedAt.slice(0, 10)
      createdAt = article.createdAt.slice(0, 10)
      articleID = articleModel.pk

      html += ` <div class="col-12 col-md-4">
              <div class="card rounded-3 mb-4" id="${articleID}">
                  <div class='article-image-container'>
                      <img
                          src="https://django-articles-app1.s3.amazonaws.com/media/${article.cover_image}"
                          class="card-img-top"
                          alt="${article.title}"
                      />
                  </div>
  
              <div class="card-body">
                  <h4 class="card-title text-center">
                  ${article.title}
                  </h4>
                  <div class="text-center mt-3 mb-1">
                      <a
                          href="/article/${articleID}"
                          class="btn btn-success rounded-pill">
                          <i class="fab fa-readme"></i> Read Now
                      </a>
                  </div>
              </div>
  
              <ul class="list-group list-group-flush">
                  <li class="list-group-item">
                      <small> Created At: ${createdAt} </small>
                  </li>
                  <li class="list-group-item">
                      <small> Last Modified At: ${modifiedAt} </small>
                  </li>
              </ul>
              </div>
          </div>
      </div>`
    })
  } else {
    html = `<h1 class="text-center text-success mt-2 mb-5">No Articles found for <span class='text-capitalize'>"${searchValue}</span>"</h1>`
  }

  return html
}
