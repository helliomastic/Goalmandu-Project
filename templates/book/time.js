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
  // month.innerHTML = `1/2/2024 <br>Chysal Futsal`;

  // update days html
  let days = "";

  var final_day = new Date();
  final_day.setDate(final_day.getDate()+9)

  var booked = new Date();
  booked.setDate(booked.getDate()+2)
  
  for (let i = 6; i < 12; i++) {
    if (booked_times.final_bookings.includes(`${i}AM`) || booked_times.final_bookings.includes(`0${i}AM`)){
      days += `<a href="#" class="day booked" id="AM-${i}">${i} - ${i+1}</a>`;
    }else{
      days += `<a href="pay/${i}AM" class="day" id="AM-${i}">${i} - ${i+1}</a>`;
    }
  }
  if (booked_times.final_bookings.includes(`12PM`)){
    days += `<a href="#" class="day booked" id="AM-12">12 - 1</a>`;
  }else{
    days += `<a href="pay/12PM" class="day" id="AM-12">12 - 1</a>`;
  }
  
  for (let i = 1; i < 8; i++) {
    if (booked_times.final_bookings.includes(`0${i}PM`)){
      days += `<a href="#" class="day booked" id="PM-${i}">${i} - ${i+1}</a>`;
    }else{
      days += `<a href="pay/0${i}PM" class="day" id="PM-${i}">${i} - ${i+1}</a>`;
    } 
    
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
