function createDateAsUTC(date) {
  return new Date(
    Date.UTC(
      date.getFullYear(),
      date.getMonth(),
      date.getDate(),
      date.getHours(),
      date.getMinutes(),
      date.getSeconds()
    )
  );
}

function convertDateToUTC(date) {
  return new Date(
    date.getUTCFullYear(),
    date.getUTCMonth(),
    date.getUTCDate(),
    date.getUTCHours(),
    date.getUTCMinutes(),
    date.getUTCSeconds()
  );
}

function search() {
  document.querySelector(".food-wrapper").innerHTML = "";
  document.getElementById("home").style.display = "none";
  document.getElementById("search").style.display = "block";
  document.querySelector(".lds-circle").style.display = "inline-block";
  
  let results = [];
  const urlParams = new URLSearchParams(window.location.search);
  console.log(urlParams.get("start"));
  console.log(urlParams.get("end"));
  console.log(urlParams.get("item"));
  let start = new Date(urlParams.get("start"));
  let end = new Date(urlParams.get("end"));
  let item = urlParams.get("item");

  let loop = new Date(start);
  let count = 0;

  while (loop <= end) {
    let date = loop.toISOString().slice(0, 10);
    console.log(date);
    for (let i = 0; i < 7; ++i) {
      ++count;
      fetch(`https://mdiner.patrickxchong.com/api/menu?item=${item}&date=${date}&location=${i}`)
        .then(response => {
          if (!response.ok) {
            throw Error(response.statusText);
          }
          return response.json();
        })
        .then(json => {
          results = results.concat(json);
          console.log(JSON.stringify(results));
          document.querySelector(".food-wrapper").innerHTML = results
            .sort((a, b) => {
              return a.date.localeCompare(b.date);
            })
            .map(result => {
              return `<a href="${result.url}" target="_blank" class="food">
          <p>${result.date}</p>
          <p>${result.location}</p>
          <p>${result.meal}</p>
          <p>${result.name}</p>
        </a>`;
            })
            .join("");

          // End condition
          if (--count === 0) {
            document.querySelector(".lds-circle").style.display = "none";
          }
        })
        .catch(error => {
          console.error("There has been a problem with Fetch:");
          console.log(error);
          // End condition
          if (--count === 0) {
            document.querySelector(".lds-circle").style.display = "none";
          }
        });
    }

    let newDate = loop.setDate(loop.getDate() + 1);
    loop = new Date(newDate);
  }
}

