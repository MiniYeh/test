let path = location.pathname;
let url = '/api/' + path;

async function attraction() {
    const response = await fetch(url).then((res) => {
        return res.json();
    });
  return response;
}

async function dotNum(response) {
    const dots = document.querySelector(".dots");
    const dotNumber = response.data.images.length;
    Array.from(Array(dotNumber)).forEach((_, index) => {
        const dot = document.createElement("li");
        dot.classList.add('dot');

        if (index === 0) dot.classList.add('dot--selected');

        dots.appendChild(dot);
    });
}

function slide() {
    let slidePosition = 0;
    const slides = document.getElementsByClassName('image');
    const dots = document.getElementsByClassName('dot');
    const slidesLength = slides.length;

    document.getElementById("right-btn").addEventListener("click", function() {
        updateSlidePosition(true);
    });
    document.getElementById("left-btn").addEventListener("click", function() {
        updateSlidePosition(false);
    });

    function updateSlidePosition(isNext = false) {
        const currentDisplay = slides[slidePosition];
        const currentDot = dots[slidePosition];
        currentDisplay.classList.remove('image--visible');
        currentDot.classList.remove('dot--selected');

        switch (isNext) {
            case true:
                slidePosition = slidePosition === slidesLength - 1
                  ? 0
                  : slidePosition + 1;
                break;
            case false:
                slidePosition = slidePosition === 0
                  ? slidesLength - 1
                  : slidePosition - 1;
                break;
            default:
                break;
        }

        slides[slidePosition].classList.add('image--visible');
        dots[slidePosition].classList.add('dot--selected');
    }
}


function updateHtml(response) {
    const main = document.querySelector("main");
    const images = document.getElementById("images");

    /**
     * img section
     */
     const attractionImages = response.data.images;
     Array.from(attractionImages).forEach((image, index) => {
        const img = document.createElement("img");
        img.setAttribute("src", image);
        img.classList.add('image');

        if (index === 0) img.classList.add('image--visible');

        images.appendChild(img);
     });

    /**
     * name section
     */
     const title = document.querySelector(".title");

     const all = document.createElement("div");
     title.appendChild(all);
     all.setAttribute("class", "all");

     const nameString = response.data["name"];
     const name = document.createElement("div");
     all.appendChild(name);
     name.setAttribute("class", "name");
     name.textContent = nameString;

     /**
     * mrt & category section
     */
     const place = document.createElement("div");
     all.appendChild(place);
     place.setAttribute("class", "place");

     const metString = response.data["mrt"];
     const mrt = document.createElement("div");
     place.appendChild(mrt);
     mrt.setAttribute("class", "mrt");
     mrt.textContent = metString;

     let at = document.createElement('div');
     at.textContent = 'at';
     at.setAttribute('class', 'at');
     place.appendChild(at);

     const categoryString = response.data["category"];
     const category = document.createElement("div");
     place.appendChild(category);
     category.setAttribute("class", "category");
     category.textContent = categoryString;

     /**
     * description & address & traffic way section
     */
     let content2 = document.createElement("div");
     content2.setAttribute("class", "content2");
     main.appendChild(content2);

     const descriptionString = response.data["description"];
     const description = document.createElement("div");
     content2.appendChild(description);
     description.setAttribute("class", "description");
     description.textContent = descriptionString;

     let attraction_address = document.createElement('div');
     attraction_address.textContent = '景點地址:';
     attraction_address.setAttribute('class', 'attraction_address');
     content2.appendChild(attraction_address);

     const addressString = response.data["address"];
     const address = document.createElement("div");
     content2.appendChild(address);
     address.setAttribute("class", "address");
     address.textContent = addressString;

     let attraction_transport = document.createElement('div');
     attraction_transport.textContent = '交通方式:';
     attraction_transport.setAttribute('class', 'attraction_transport');
     content2.appendChild(attraction_transport);

     const transportString = response.data["transport"];
     const transport = document.createElement("div");
     content2.appendChild(transport);
     transport.setAttribute("class", "transport");
     transport.textContent = transportString;
}

function check(n) {
    let morningBtn = document.querySelector("#input_time1");
    let afternoonBtn = document.querySelector("#input_time2");
    let money = document.querySelector(".money");
    if (n == 1) {
        morningBtn.style.backgroundColor = "#448899";
        afternoonBtn.style.backgroundColor = "#FFFFFF";
        money.textContent = "新台幣 2000 元";
    } else if (n == 2) {
        morningBtn.style.backgroundColor = "#FFFFFF";
        afternoonBtn.style.backgroundColor = "#448899";
        money.textContent = "新台幣 2500 元";
    }
}

async function main() {
    const response = await attraction();
    updateHtml(response);
    dotNum(response);
    slide();
}

main();
