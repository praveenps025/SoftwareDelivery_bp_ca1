// k6 load test, run by the deploy pipeline against the stage site.
//   k6 run -e BASE_URL=https://<site> tests/performance/load-test.js
// Kept light (10 users, about 1 minute) because stage runs on the App Service
// F1 plan, which has a daily CPU quota.
import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = (__ENV.BASE_URL || "http://localhost:5000").replace(/\/$/, "");

// same readings as the unit tests, one per category
const READINGS = [
  { systolic: 85, diastolic: 55, category: "Low Blood Pressure" },
  { systolic: 110, diastolic: 70, category: "Ideal Blood Pressure" },
  { systolic: 125, diastolic: 82, category: "Pre-High Blood Pressure" },
  { systolic: 145, diastolic: 92, category: "High Blood Pressure" },
];

export const options = {
  stages: [
    { duration: "15s", target: 10 }, // ramp up
    { duration: "30s", target: 10 }, // hold
    { duration: "15s", target: 0 },  // ramp down
  ],
  // missing any of these fails the stage job, so production is not deployed
  thresholds: {
    http_req_duration: ["p(95)<1000"], // 95% of requests under 1 second
    http_req_failed: ["rate<0.01"],    // under 1% failed requests
    checks: ["rate>0.99"],             // pages load and show the right category
  },
};

export default function () {
  const page = http.get(`${BASE_URL}/`);
  check(page, { "calculator page loads": (r) => r.status === 200 });

  // CSRF is on outside the Testing config, so submit the token from the form like a browser
  const token = page.html().find("input[name=csrf_token]").attr("value");
  const reading = READINGS[Math.floor(Math.random() * READINGS.length)];
  const result = http.post(
    `${BASE_URL}/`,
    { csrf_token: token, "BP.Systolic": reading.systolic, "BP.Diastolic": reading.diastolic },
    { headers: { Referer: `${BASE_URL}/` } },
  );
  check(result, {
    "reading gets the right category": (r) => r.status === 200 && r.body.includes(reading.category),
  });

  if (Math.random() < 0.2) {
    const privacy = http.get(`${BASE_URL}/Privacy`);
    check(privacy, { "privacy page loads": (r) => r.status === 200 });
  }

  sleep(1);
}
