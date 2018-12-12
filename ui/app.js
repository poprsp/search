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
        const urlSplit = decodeURIComponent(item.url).split("/");
        a.appendChild(document.createTextNode(urlSplit[urlSplit.length - 1]));
        a.setAttribute("href", item.url);
        url.appendChild(a);
        row.appendChild(url);

        const score = document.createElement("td");
        const scoreFixed = item.score.total.toFixed(2);
        score.appendChild(document.createTextNode(scoreFixed));
        row.appendChild(score);

        const content = document.createElement("td");
        const contentFixed = item.score.content.toFixed(2);
        content.appendChild(document.createTextNode(contentFixed));
        row.appendChild(content);

        const location = document.createElement("td");
        const locationFixed = item.score.location.toFixed(2);
        location.appendChild(document.createTextNode(locationFixed));
        row.appendChild(location);

        const pageRank = document.createElement("td");
        const pageRankFixed = item.score.page_rank.toFixed(2);
        pageRank.appendChild(document.createTextNode(pageRankFixed));
        row.appendChild(pageRank);

        result.appendChild(row);
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
