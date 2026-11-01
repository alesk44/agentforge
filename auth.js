import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = "https://fopiwzdpvhndgssxoljf.supabase.co";
const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_sZEUuSN1klJMtS26vKPLbg_f-D6fJjS";
const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
});

const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);
let mode = params.get("mode") === "signup" ? "signup" : "login";
const dashboardUrl = new URL("./dashboard.html", location.href).href;
const authUrl = new URL("./auth.html", location.href).href;

function notice(message, kind = "info") {
  $("notice").hidden = false;
  $("notice").textContent = message;
  $("notice").className = "notice " + kind;
}
function setMode(next) {
  mode = next;
  $("formTitle").textContent = mode === "signup" ? "Create your account." : "Welcome back.";
  $("formIntro").textContent = mode === "signup" ? "Set up your secure AgentForge workspace." : "Sign in to continue to your AgentForge workspace.";
  $("submitButton").textContent = mode === "signup" ? "Create account" : "Sign in";
  $("password").autocomplete = mode === "signup" ? "new-password" : "current-password";
  $("nameField").hidden = mode !== "signup";
  $("forgotButton").hidden = mode !== "login";
  $("switchLine").innerHTML = mode === "signup"
    ? 'Already have an account? <a href="./auth.html" id="switchLink">Sign in</a>'
    : 'New to AgentForge? <a href="./auth.html?mode=signup" id="switchLink">Create an account</a>';
}
setMode(mode);

const { data: initial } = await supabase.auth.getSession();
if (initial.session) location.replace(dashboardUrl);

$("authForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const email = $("email").value.trim();
  const password = $("password").value;
  const submit = $("submitButton");
  submit.disabled = true;
  submit.textContent = mode === "signup" ? "Creating account…" : "Signing in…";
  try {
    if (mode === "signup") {
      const { data, error } = await supabase.auth.signUp({
        email, password,
        options: { data: { display_name: $("fullName").value.trim() } }
      });
      if (error) throw error;
      if (data.session) location.replace(dashboardUrl);
      else notice("Account created. Check your inbox to confirm your email, then return here to sign in.", "success");
    } else {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) throw error;
      location.replace(dashboardUrl);
    }
  } catch (error) {
    notice(error.message || "Something went wrong. Please try again.", "error");
  } finally {
    submit.disabled = false;
    submit.textContent = mode === "signup" ? "Create account" : "Sign in";
  }
});

$("googleButton").addEventListener("click", async () => {
  $("googleButton").disabled = true;
  try {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: dashboardUrl }
    });
    if (error) throw error;
  } catch (error) {
    notice(error.message || "Google sign-in is not available yet.", "error");
    $("googleButton").disabled = false;
  }
});

$("forgotButton").addEventListener("click", async () => {
  const email = $("email").value.trim();
  if (!email) return notice("Enter your email address first.", "error");
  try {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: authUrl + "?mode=recovery"
    });
    if (error) throw error;
    notice("If this email is registered, a password reset link will arrive shortly.", "success");
  } catch (error) {
    notice(error.message || "Could not request a password reset.", "error");
  }
});

if (params.get("mode") === "recovery") {
  $("formTitle").textContent = "Check your email.";
  notice("Use the password reset link from your email to return here and set a new password.", "info");
}
