document.addEventListener("DOMContentLoaded", function() {
  const starter = document.getElementById("upload");
  starter.addEventListener("click", start_set, false);

  function start_set(){//start状態
    start_go()
  }

  function start_go(){//start押下
    const loader = document.querySelector("#loader.predict_loader");
    loader.classList.add('show');
  }
})

