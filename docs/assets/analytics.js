// Set this to the public measurement ID from the site's GA4 web stream.
const measurementId = "";
const preferenceKey = "site-analytics-enabled";
const controls = document.querySelector("#analytics-controls");

function readPreference() {
  try {
    return localStorage.getItem(preferenceKey) === "yes";
  } catch {
    return false;
  }
}

function loadAnalytics() {
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }

  gtag("consent", "default", {
    analytics_storage: "granted",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
  });
  gtag("js", new Date());
  gtag("config", measurementId);

  const script = document.createElement("script");
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
  document.head.append(script);
}

if (controls && /^G-[A-Z0-9]+$/.test(measurementId)) {
  let enabled = readPreference();
  const button = document.createElement("button");
  button.type = "button";
  button.className = "analytics-button";
  button.textContent = "Allow Google Analytics";
  button.setAttribute("aria-pressed", String(enabled));
  controls.append(button);

  if (enabled) loadAnalytics();

  button.addEventListener("click", () => {
    enabled = !enabled;
    button.setAttribute("aria-pressed", String(enabled));
    try {
      localStorage.setItem(preferenceKey, enabled ? "yes" : "no");
    } catch {
      // The choice still applies to this page when browser storage is blocked.
    }

    window[`ga-disable-${measurementId}`] = !enabled;
    if (enabled && !window.dataLayer) loadAnalytics();
  });
}
