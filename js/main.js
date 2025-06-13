/* Animacioón de los botones chulos */

const buttons = document.querySelectorAll('.btn');
buttons.forEach(btn => {
  btn.addEventListener('click', function(btn) {
    
    let x = btn.clientX - btn.target.offsetLeft;
    let y = btn.clientY - btn.target.offsetTop;
    
    let onda = document.createElement('span');
    onda.style.left = x + 'px';
    onda.style.top = y + 'px';
    this.appendChild(onda);
    
    setTimeout(() => {
      onda.remove()
    }, 1000);
  });
});


/* Bio scrolleable */

let sections = document.querySelectorAll ('.bio');

window.onscroll = () => {
  sections.forEach(sec => {
    let top = window.scrollY;
    let  offset = sec.offsetTop -150;
    let height = sec.offsetHeight;

    if (top >= offset && top < offset + height) {
      sec.classList.add('show-animate');
    } else {
      sec.classList.remove('show-animate');
    }
  })
}

/* Efecto escritura */

var TxtType = function(el, toRotate, period) {
  this.toRotate = toRotate;
  this.el = el;
  this.loopNum = 0;
  this.period = parseInt(period, 100) || 1200;
  this.txt = '';
  this.tick();
  this.isDeleting = false;
};

TxtType.prototype.tick = function() {
  var i = this.loopNum % this.toRotate.length;
  var fullTxt = this.toRotate[i];

  if (this.isDeleting) {
  this.txt = fullTxt.substring(0, this.txt.length - 6);
  } else {
  this.txt = fullTxt.substring(0, this.txt.length + 5);
  }

  this.el.innerHTML = '<span class="wrap">'+this.txt+'</span>';

  var that = this;
  var delta = 200 - Math.random() * 100;

  if (this.isDeleting) { delta /= 2; }

  if (!this.isDeleting && this.txt === fullTxt) {
  delta = this.period;
  this.isDeleting = true;
  } else if (this.isDeleting && this.txt === '') {
  this.isDeleting = false;
  this.loopNum++;
  delta = 500;
  }

  setTimeout(function() {
  that.tick();
  }, delta);
};

window.onload = function() {
  var elements = document.getElementsByClassName('typewrite');
  for (var i=0; i<elements.length; i++) {
      var toRotate = elements[i].getAttribute('data-type');
      var period = elements[i].getAttribute('data-period');
      if (toRotate) {
        new TxtType(elements[i], JSON.parse(toRotate), period);
      }
  }
  // INJECT CSS
  var css = document.createElement("style");
  css.type = "text/css";
  css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #fff}";
  document.body.appendChild(css);
};

/* Menú hamburguesa */

function showSidebar(){
  const sidebar = document.querySelector('.sidebar')
  sidebar.style.display = 'flex'
}

function hideSidebar(){
  const sidebar = document.querySelector('.sidebar')
  sidebar.style.display = 'none'
}

/* Carrusel */

const initSlider = () => {
  const listaCarrusel = document.querySelector(".contenedor-carrusel .lista-carrusel");
  const slideButtons = document.querySelectorAll(".contenedor-carrusel .slide-button");

/* Que el carrusel se mueva dependiendo de a qué botón le hacemos click */
  slideButtons.forEach(button => {
    button.addEventListener("click", () => {
      const direction =  button.id === "btn-iz" ? -0.5 : 0.5;
      const scrollAmount = listaCarrusel.clientWidth * direction;
      listaCarrusel.scrollBy({ left: scrollAmount, behavior: "smooth" });
    })
  })
}

window.addEventListener("load", initSlider);

/* Interruptor */

var btn = document.getElementById('btn')

var header = document.getElementById('header')

var compra = document.getElementById('compra')

function leftClick() {
  btn.style.left = '0'
  document.getElementById('fondo').src="../assets/Portfolio/YoDef.png";
  header.style.backgroundColor = "#fff";
  compra.style.backgroundColor = "#fff";

  const spans = document.querySelectorAll('span');
  spans.forEach((span) => {
    span.style.setProperty('--span-visibilidad', 'hidden');
  });
}

const spans = document.querySelectorAll('span');
spans.forEach((span) => {
  span.style.setProperty('--span-visibilidad', 'hidden');
});

function rightClick() {
  btn.style.left = '102px'
  document.getElementById('fondo').src="../assets/Portfolio/YoChulo.png";  
  header.style.backgroundColor = "#fff";
  compra.style.backgroundColor = "#fff";
  
  const spans = document.querySelectorAll('span');
spans.forEach((span) => {
  span.style.setProperty('--span-visibilidad', 'visible');
});
}

gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

ScrollTrigger.defaults({
  toggleActions: "play none none reverse",
  markers: true
});

gsap.utils.toArray(".panel").forEach((panel, i) => {
  ScrollTrigger.create({
    trigger: panel,
    start: "top top",
    end: "+=100%",
    pin: true, 
    pinSpacing: false,
    scrub: 1,
    snap: {
       snapTo: 1,
       duration: {min: 0.5, max: 0.5}
    }
  });
});

gsap.utils.toArray("nav a").forEach(function(a) {
  a.addEventListener("click", function(e) {
    e.preventDefault();
    gsap.to(window, {duration: 1, scrollTo: e.target.getAttribute("href")});
  });
});