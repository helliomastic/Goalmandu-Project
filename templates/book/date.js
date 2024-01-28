const daysContainer = document.querySelector(".days"),
  nextBtn = document.querySelector(".next-btn"),
  prevBtn = document.querySelector(".prev-btn"),
  month = document.querySelector(".month"),
  todayBtn = document.querySelector(".today-btn");

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const booking_allowed = 7;

// get current date
const date = new Date();

// get current month
let currentMonth = date.getMonth();

// get current year
let currentYear = date.getFullYear();

// function to render days
function renderCalendar() {
  // get prev month current month and next month days
  date.setDate(1);
  const firstDay = new Date(currentYear, currentMonth, 1);
  const lastDay = new Date(currentYear, currentMonth + 1, 0);
  const lastDayIndex = lastDay.getDay();
  const lastDayDate = lastDay.getDate();
  const prevLastDay = new Date(currentYear, currentMonth, 0);
  const prevLastDayDate = prevLastDay.getDate();
  const nextDays = 7 - lastDayIndex - 1;

  // update current year and month in header
  month.innerHTML = `${months[currentMonth]} ${currentYear}`;

  // update days html
  let days = "";

  // prev days html 
  for (let x = firstDay.getDay(); x > 0; x--) {
    days += `<div class="day prev">${prevLastDayDate - x + 1}</div>`;
  }
  var final_day = new Date();
  final_day.setDate(final_day.getDate()+7)  

  // current month days
  for (let i = 1; i <= lastDayDate; i++) {
    // check if its today then add today class
    var y = new Date().getFullYear();
    var m = new Date().getMonth()+1;
    var d = new Date().getDate();

    if (
      i === new Date().getDate() &&
      currentMonth === new Date().getMonth() &&
      currentYear === new Date().getFullYear()
    ) {
      // if date month year matches add today
      days += `<a href="/pick-time/${futsal_id}/${y}/${m}/${i}/" class="day today">${i}</a>`;
    } 
     else if (currentMonth != new Date().getMonth())
      {
      days += `<a class="day muted">${i}</a>`;
      }
     else if (
      // if it is for not in next 7 days
      i >= final_day.getDate() &&
      currentMonth === new Date().getMonth() &&
      currentYear === new Date().getFullYear())
      {
      days += `<a class="day muted">${i}</a>`;
      }
     else if (
      // if it is for not in next 7 days
      i < d &&
      currentMonth === new Date().getMonth() &&
      currentYear === new Date().getFullYear())
      {
      days += `<a class="day muted">${i}</a>`;
      }
    //  else if (
    //   // if it is booked
    //   i === booked.getDate() &&
    //   currentMonth === new Date().getMonth() &&
    //   currentYear === new Date().getFullYear())
    //   {
    //   days += `<a href="#" class="day booked">${i}</a>`;
    //   }
    else {
      //else dont add today
      days += `<a href="/pick-time/${futsal_id}/${y}/${m}/${i}/" class="day">${i}</a>`;
    }
  }

  // next MOnth days
  for (let j = 1; j <= nextDays; j++) {
    days += `<a class="day muted">${j}</a>`;
  }

  // run this function with every calendar render
  hideTodayBtn();
  daysContainer.innerHTML = days;
}

renderCalendar();

nextBtn.addEventListener("click", () => {
  // increase current month by one
  currentMonth++;
  if (currentMonth > 11) {
    // if month gets greater that 11 make it 0 and increase year by one
    currentMonth = 0;
    currentYear++;
  }
  // rerender calendar
  renderCalendar();
});

// prev monyh btn
prevBtn.addEventListener("click", () => {
  // increase by one
  currentMonth--;
  // check if let than 0 then make it 11 and deacrease year
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  renderCalendar();
});

// go to today
todayBtn.addEventListener("click", () => {
  // set month and year to current
  currentMonth = date.getMonth();
  currentYear = date.getFullYear();
  // rerender calendar
  renderCalendar();
});

// lets hide today btn if its already current month and vice versa

function hideTodayBtn() {
  if (
    currentMonth === new Date().getMonth() &&
    currentYear === new Date().getFullYear()
  ) {
    todayBtn.style.display = "none";
  } else {
    todayBtn.style.display = "flex";
  }
}