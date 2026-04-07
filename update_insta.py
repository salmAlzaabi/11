import instaloader
import json
import os
from datetime import datetime

# الأرقام التعريفية للحسابات (IDs)
ACCOUNTS = [36861409878, 34831997508]

def update_data():
    L = instaloader.Instaloader()
    
    # محاولة تحميل البيانات القديمة للمقارنة
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)
    except:
        old_data = {"profiles": [], "logs": []}

    new_profiles = []
    logs = old_data.get("logs", [])

    for user_id in ACCOUNTS:
        try:
            p = instaloader.Profile.from_id(L.context, user_id)
            current_profile = {
                "id": user_id,
                "username": p.username,
                "full_name": p.full_name,
                "bio": p.biography,
                "followers": p.followers,
                "pfp": p.profile_pic_url
            }
            new_profiles.append(current_profile)

            # المقارنة مع البيانات السابقة لتسجيل الـ Logs
            old_p = next((item for item in old_data["profiles"] if item["id"] == user_id), None)
            
            if old_p:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                # إذا تغير البايو
                if old_p["bio"] != current_profile["bio"]:
                    logs.append(f"[{timestamp}] @{p.username}: تم تغيير البايو")
                # إذا تغير اسم المستخدم
                if old_p["username"] != current_profile["username"]:
                    logs.append(f"[{timestamp}] ايدي {user_id}: تغير اليوزر من @{old_p['username']} إلى @{p.username}")
        except Exception as e:
            print(f"Error fetching {user_id}: {e}")
            continue

    # حفظ البيانات (نحتفظ بآخر 15 سجل فقط)
    final_data = {
        "profiles": new_profiles,
        "logs": logs[-15:]
    }
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update_data()
