from db.session import get_db_connection
from crud.utils import rows_to_dict
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def get_user_skills(cursor,user_id):
    try:
        cursor.execute("SELECT name,category FROM skills WHERE id in (SELECT skill_id FROM user_skills WHERE user_id = ?)", (user_id,))
        skills = rows_to_dict(cursor, cursor.fetchall())
        output = {}
        for skill in skills:
            output[skill['category']] = output.get(skill['category'], []) + [skill['name']]
        return output
    except Exception as e:
        raise Exception("Error fetching user skills: " + str(e))

def get_user_experience(cursor,user_id):
    try:
        cursor.execute("SELECT id, company_name, job_title, location, start_date, end_date FROM experience WHERE user_id = ? ORDER BY start_date DESC", (user_id,))
        experience = cursor.fetchall()
        return rows_to_dict(cursor, experience)
    except Exception as e:
        raise Exception("Error fetching user experience: " + str(e))

def get_user_info(cursor,user_id):
    try:
        cursor.execute("SELECT name,description, email,linkedin,github,dp_image_path FROM users WHERE id = ?", (user_id,))
        user_info = cursor.fetchone()
        output = rows_to_dict(cursor, [user_info])[0]
        output['dp_image_path'] = 'https://praveenazurelearn.blob.core.windows.net/azureimages' + output['dp_image_path'] if output['dp_image_path'] else None
        return output
    except Exception as e:
        raise Exception("Error fetching user info: " + str(e))

def get_user_projects(cursor,user_id):
    try:
        cursor.execute("select p.id,p.title as name,p.description,p.github_link,t.name as tool_name from projects p left join project_tools pt on p.id = pt.project_id left join tools t on pt.tool_id = t.id where p.user_id = ?", (user_id,))
        projects = rows_to_dict(cursor, cursor.fetchall())
        output = {}
        for project in projects:
            project_id = project['id']
            if project_id not in output:
                output[project_id] = {
                    'name': project['name'],
                    'description': project['description'],
                    'github_link': project['github_link'],
                    'tools': []
                }
            if project['tool_name']:
                output[project_id]['tools'].append(project['tool_name'])
        return list(output.values())
    except Exception as e:
        raise Exception("Error fetching user projects: " + str(e))  


def get_user_profile_db(user_id):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        output = {}
        output['user_info'] = get_user_info(cursor,user_id)
        output['user_skills'] = get_user_skills(cursor,user_id)
        output['user_experience'] = get_user_experience(cursor,user_id)
        output['user_projects'] = get_user_projects(cursor,user_id)
        return JSONResponse(content=jsonable_encoder(output), status_code=200)
    except Exception as e:
        raise e
    finally:
        db.close()

def get_user_experience_details_db(experience_id):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT e.id, e.description,s.name as skill FROM experience e inner join experience_skills es on e.id = es.experience_id inner join skills s on es.skill_id = s.id WHERE e.id = ?", (experience_id,))
        experience = rows_to_dict(cursor, cursor.fetchall())
        output = {}
        for exp in experience:
            output[exp['id']] = {
                'id'   : exp['id'],
                'description': exp['description'],
                'skills': output.get(exp['id'], {}).get('skills', []) + [exp['skill']]
            }
        if not output:
            return JSONResponse(content={"error": "Experience not found"}, status_code=404)
        return JSONResponse(content=jsonable_encoder(list(output.values())), status_code=200)
    except Exception as e:
        raise e
    finally:
        db.close()
