import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = "https://fopiwzdpvhndgssxoljf.supabase.co";
const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_sZEUuSN1klJMtS26vKPLbg_f-D6fJjS";
const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
});
const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);
let mode = params.get("mode") === "signup" ? "signup" : (params.get("mode") === "recovery" ? "recovery" : "login");
const dashboardUrl = new URL("./dashboard.html", location.href).href;
const authUrl = new URL("./auth.html", location.href).href;

function notice(message, kind = "info") {
  $("notice").hidden = false;
  $("notice").textContent = message;
  $("notice").className = "notice " + kind;
}
function setMode(next) {
  mode = next;
  const recovery = mode === "recovery";
  $("formTitle").textContent = recovery ? "Choose a new password." : (mode === "signup" ? "Create your account." : "Welcome back.");
  $("formIntro").textContent = recovery ? "Set a new password for your AgentForge account." : (mode === "signup" ? "Set up your secure AgentForge workspace." : "Sign in to continue to your AgentForge workspace.");
  $("submitButton").textContent = recovery ? "Update password" : (mode === "signup" ? "Create account" : "Sign in");
  $("password").autocomplete = mode === "login" ? "current-password" : "new-password";
  $("nameField").hidden = mode !== "signup";
  $("email").hidden = recovery;
  $("email").previousElementSibling.hidden = recovery;
  $("forgotButton").hidden = mode !== "login";
  $("switchLine").hidden = recovery;
}
setMode(mode);

const { data: initial } = await supabase.auth.getSession();
if (initial.session && mode !== "recovery") location.replace(dashboardUrl);

$("authForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const email = $("email").value.trim();
  const password = $("password").value;
  const submit = $("submitButton");
  submit.disabled = true;
  try {
    if (mode === "recovery") {
      submit.textContent = "Updating password…";
      const { error } = await supabase.auth.updateUser({ password });
      if (error) throw error;
      notice("Password updated. You can now sign in with your new password.", "success");
      $("authForm").reset();
      setMode("login");
    } else if (mode === "signup") {
      submit.textContent = "Creating account…";
      const { data, error } = await supabase.auth.signUp({
        email, password,
        options: {
          data: { display_name: $("fullName").value.trim() },
          emailRedirectTo: dashboardUrl
        }
      });
      if (error) throw error;
      if (data.session) location.replace(dashboardUrl);
      else notice("Account created. Check your inbox to confirm your email, then return here to sign in.", "success");
    } else {
      submit.textContent = "Signing in…";
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) throw error;
      location.replace(dashboardUrl);
    }
  } catch (error) {
    notice(error.message || "Something went wrong. Please try again.", "error");
  } finally {
    submit.disabled = false;
    submit.textContent = mode === "recovery" ? "Update password" : (mode === "signup" ? "Create account" : "Sign in");
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

if (mode === "recovery") notice("Enter your new password below.", "info");
