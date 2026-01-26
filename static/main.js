function openMenu(){
  document.getElementById("drawer").classList.add("open");
  document.getElementById("overlay").style.display="block";
}

function closeMenu(){
  document.getElementById("drawer").classList.remove("open");
  document.getElementById("overlay").style.display="none";
}
