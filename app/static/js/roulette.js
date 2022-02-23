document.addEventListener("DOMContentLoaded", function() {
  const starter = document.getElementById("start");
  starter.addEventListener("click", start_set, false);
  //要素の表示、円周上に表示させる
  let num = [0,1,2,3,4];
  let roulette = document.getElementById("roulette");
  /*円形に並べる*/
  let item_length = num.length;
  //rouletteの半径を計算
  let r = roulette.clientWidth / 3;
  //360度÷配置要素数
  let deg = 360.0 / item_length;
  //さっきの角度をラジアンに変更
  const rad = (deg * Math.PI / 180.0);
  //
  let arr_img = ['/static/images/roulette/roulette_0.png',
    '/static/images/roulette/roulette_1.png',
    '/static/images/roulette/roulette_2.png',
    '/static/images/roulette/roulette_3.png',
    '/static/images/roulette/roulette_4.png'];
  //要素追加して表示させる
  for (var i = 0; i < num.length; i++ ){
      let img = document.createElement('img');
      img.className = "cil";
      img.id = "cil"+ i;
      img.innerHTML= num[i];
      img.src = arr_img[i];
      const x = Math.cos(rad * i + rad/4) * r + r;
      const y = Math.sin(rad * i + rad/4) * r + r;
      let circle = roulette.appendChild(img);
      circle.style.left = x + "px";
      circle.style.top = y + "px";
  }    
  let interval;
  let first = false;
  let number = 1;
  let counter = 2;
  let grid =0;

  function start_set() {//start状態
      if (first === false) {
          interval = setInterval(start_go, 50);
          first = true;
          starter.addEventListener("click", stop_set, false);
      }
  }

  function start_go() {//start押下
      for (var k = 0; k < item_length; k++) {
          const div_number = document.getElementById('cil' + [k]);//表示上のidの取得
          div_number.classList.remove('red');//.redを消す
      }
      grid = counter++ % 5;
      number = num[grid];//.redをつけるためのランダムな数字を選択
      div_number = document.getElementById('cil'+ number);
      div_number.classList.add('red');
  }

  function stop_set() {//stop押下
    clearInterval(interval);
    first = false;
    const red_number = document.querySelector('.red');//.redクラスのついているものを取得
    const id = red_number.id
    commenterNum = id.replace('cil', '')
    document.getElementById("commenterNumInput").value = commenterNum;
    setTimeout(function() {
        const formElement = document.forms[0];
        formElement.submit();
        return false;
    }, 2000);
  }
})
