"use strict";

function search(query) {
  if (query.length === 0) {
    return;
  }

  const result = document.getElementById("result");

  /* Remove all children except for the header */
  while (result.children.length > 1) {
    result.removeChild(result.children[1]);
  }

  fetch(`${window.location.origin}/api/search/${query}/5`)
    .then(res => {
      return res.json();
    })
    .then(json => {
      for (const item of json) {
        const row = document.createElement("tr");

        const url = document.createElement("td");
        const a = document.createElement("a");
        const urlSplit = item.url.split("/");
        a.appendChild(document.createTextNode(urlSplit[urlSplit.length - 1]));
        a.setAttribute("href", item.url);
        url.appendChild(a);
        row.appendChild(url);

        const score = document.createElement("td");
        const scoreFixed = item.scores.total.toFixed(2);
        score.appendChild(document.createTextNode(scoreFixed));
        row.appendChild(score);

        const content = document.createElement("td");
        const contentFixed = item.scores.content.toFixed(2);
        content.appendChild(document.createTextNode(contentFixed));
        row.appendChild(content);

        const location = document.createElement("td");
        const locationFixed = item.scores.location.toFixed(2);
        location.appendChild(document.createTextNode(locationFixed));
        row.appendChild(location);

        result.appendChild(row);
        console.log(item);
      }
    });
}

function addFormListener() {
  document.getElementById("form").addEventListener("submit", e => {
    search(document.getElementById("query").value);
  });
}

function main() {
  addFormListener();
}

window.onload = main;
