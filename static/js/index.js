let keyword = '';
let page = 0;
let isFetchingMore = false;
let noData = false;

function removeMainHtml() {
  const main = document.querySelector("main");
  main.childNodes.forEach(child => {
    main.removeChild(child);
  });
}

// call attractions api
async function attractions() {
  if (isFetchingMore || noData) return null;

  console.log("fetching!");
  isFetchingMore = true;

  const src = `/api/attractions?page=${page}${
    keyword !== '' ? `&keyword=${keyword}` : ''
  }`;

  const response = await fetch(src).then((res) => {
    page += 1;
    isFetchingMore = false;
    return res.json();
  });

  if (response.data.length === 0) {
    noData = true;
  }
  
  if (
    noData && // 1. 當下沒有資料
    keyword !== '' && // 2. 有關鍵字
    document.querySelectorAll('.all').length === 0 // 3. content 裡面原本就無資料 (不只是單單這一個 page 沒有資料)
  ) {
    document.querySelector('main').innerHTML = `搜尋不到 ${keyword} 的相關資料。`
   }

  return response;
}

function updateHtml(response) {
  if (response === null || noData) return;

  const main = document.querySelector("main");
  let content = document.querySelector(".content");

  if (!content) {
    content = document.createElement("div");
    content.setAttribute("class", "content");
    main.appendChild(content);
  }

  Array.from(response.data).forEach((_, index) => {
    /**
     * all section
     */
    const all = document.createElement("div");
    content.appendChild(all);
    all.setAttribute("class", "all");

    /**
     * img section
     */
    const myString = response.data[index]["images"][0];
    const img = document.createElement("img");
    all.appendChild(img);
    img.setAttribute("src", myString);
    img.setAttribute("class", "img");

    /**
     * name section
     */
    const title = document.createElement("div");
    all.appendChild(title);
    title.setAttribute("class", "title");

    const nameString = response.data[index]["name"];
    const name = document.createElement("div");
    title.appendChild(name);
    name.setAttribute("class", "name");
    name.textContent = nameString;

    const categoryString = response.data[index]["category"];
    const category = document.createElement("div");
    title.appendChild(category);
    category.setAttribute("class", "category");
    category.textContent = categoryString;

    const metString = response.data[index]["mrt"];
    const mrt = document.createElement("div");
    title.appendChild(mrt);
    mrt.setAttribute("class", "mrt");
    mrt.textContent = metString;
  });
}

/**　https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API */
function createObserver() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(async (entry) => {
        if (entry.isIntersecting) {
          // 拉新的資料
          const res = await attractions();
          updateHtml(res);
          console.log("Done!");
        }
      });
    },
    {
      root: null,
      rootMargin: "0px",
      threshold: 0,
    }
  );

  return observer;
}

async function main() {
  const observer = createObserver();
  observer.observe(document.querySelector("footer"));

  const inputElement = document.getElementById('ins');
  inputElement.addEventListener('input', (event) => {
    keyword = event.target.value;
  });

  const submitButtonElement = document.getElementById("but");
  submitButtonElement.addEventListener("click", async function(event){
    event.preventDefault();
    removeMainHtml();
    page = 0;
    noData = false;
    const response = await attractions();
    updateHtml(response);
  });
}

main();
