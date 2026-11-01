import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
const supabase = createClient("https://fopiwzdpvhndgssxoljf.supabase.co","sb_publishable_sZEUuSN1klJMtS26vKPLbg_f-D6fJjS",{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});
const $=id=>document.getElementById(id);
function status(message,kind="info"){$("status").hidden=false;$("status").textContent=message;$("status").className="notice "+kind;}
const {data:{session}}=await supabase.auth.getSession();
if(!session){location.replace(new URL("./auth.html",location.href).href);}
else{
  $("welcome").textContent="Welcome"+(session.user.user_metadata?.display_name?" back, "+session.user.user_metadata.display_name:".");
  await loadBusinesses();
}
async function loadBusinesses(){
 const {data,error}=await supabase.from("businesses").select("id,name,industry,created_at").order("created_at",{ascending:false});
 if(error){$("businessList").innerHTML="";status("Could not load your businesses: "+error.message,"error");return;}
 $("businessList").innerHTML="";
 if(!data.length){$("businessList").innerHTML='<p class="muted">No business workspace yet. Create your first one below.</p>';return;}
 for(const business of data){const el=document.createElement("article");el.className="business-item";const name=document.createElement("strong");name.textContent=business.name;const meta=document.createElement("small");meta.textContent=business.industry||"Business workspace";el.append(name,meta);$("businessList").append(el);}
}
$("businessForm").addEventListener("submit",async event=>{
 event.preventDefault();const button=event.currentTarget.querySelector("button");button.disabled=true;button.textContent="Creating…";
 const {data:{user}}=await supabase.auth.getUser();
 const {error}=await supabase.from("businesses").insert({owner_id:user.id,name:$("businessName").value.trim(),industry:$("industry").value.trim()||null});
 if(error)status("Could not create workspace: "+error.message,"error");else{$("businessName").value="";$("industry").value="";status("Business workspace created.","success");await loadBusinesses();}
 button.disabled=false;button.textContent="Create business workspace";
});
$("signOut").addEventListener("click",async()=>{await supabase.auth.signOut();location.replace(new URL("./auth.html",location.href).href);});
