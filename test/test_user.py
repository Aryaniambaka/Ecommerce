import pytest


def test_Get_current_user(authorized_client,fixtureuser):
    response= authorized_client.get("/user/current")
    data=response.json()
    print(data)

    assert data["id"]==fixtureuser["id"]
    assert data["email"]==fixtureuser["email"]
    assert response.status_code==200
def test_current_user_unauthorized(fixtureuser,client):
    response = client.get("/user/current")

    assert response.status_code == 401
@pytest.mark.parametrize("email,password",[
    ("lol@gmail.com","string123"),
    ("lol1@gmail.com","123")
])
def test_auth(client,email,password):
    form_data={
        "username":email,"password":password
    }
    response=client.post("/login/verification",data=form_data)
    assert response.status_code == 403
