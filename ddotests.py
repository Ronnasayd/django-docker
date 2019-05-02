import unittest
import config

class TestStringMethods(unittest.TestCase):

    def test_debug(self):
        self.assertIsInstance(config.DEBUG, bool)
    
    def test_frontdevtools(self):
        self.assertIsInstance(config.FRONT_DEV_TOOLS,bool)
    
    def test_requirements(self):
        self.assertIsInstance(config.REQUIREMENTS,list)
        for requirement in config.REQUIREMENTS:
            self.assertIsInstance(requirement,str)
    
    def test_projectname(self):
        self.assertIsInstance(config.PROJECT_NAME,str)
    
    def test_python_version(self):
        self.assertIsInstance(config.PYTHON_VERSION,str)
    
    def test_django_version(self):
        self.assertIsInstance(config.DJANGO_VERSION,str)
    
    def test_web_commands_build(self):
        self.assertIsInstance(config.WEB_COMMANDS_BUILD,list)
    
    def test_database_image(self):
        self.assertIsInstance(config.DATABASE_IMAGE,str)
    
    def test_database_external(self):
        self.assertIsInstance(config.DATABASE_EXTERNAL,bool)
    
    def test_database_default_enviroments(self):
        self.assertIsInstance(config.DATABASE_DEFAULT_ENVIROMENTS,dict)
        for key,value in config.DATABASE_DEFAULT_ENVIROMENTS.items():
            self.assertIsInstance(key,str)
            self.assertIsInstance(value,str)
    
    def test_database_other_enviroments(self):
        self.assertIsInstance(config.DATABASE_OTHERS_ENVIROMENTS,dict)
        for key,value in config.DATABASE_OTHERS_ENVIROMENTS.items():
            self.assertIsInstance(key,str)
            self.assertIsInstance(value,str)
    
    def test_database_root(self):
        self.assertIsInstance(config.DATABASE_ROOT,dict)
        for key,value in config.DATABASE_ROOT.items():
            self.assertIsInstance(key,str)
            self.assertIsInstance(value,str)
    
    def test_database_engine(self):
        self.assertIsInstance(config.DATABASE_ENGINE,str)
    
    def test_web_port(self):
        self.assertIsInstance(config.WEB_PORT,str)
        self.assertIsInstance(int(config.WEB_PORT),int)
    
    def test_nginx_port(self):
        self.assertIsInstance(config.NGINX_PORT,str)
        self.assertIsInstance(int(config.NGINX_PORT),int)
    
    def test_database_external_port(self):
        self.assertIsInstance(config.DATABASE_EXTERNAL_PORT,str)
        self.assertIsInstance(int(config.DATABASE_EXTERNAL_PORT),int)
    
    def test_web_enviroment(self):
        self.assertIsInstance(config.WEB_ENVIROMENT,dict)
        for key,value in config.WEB_ENVIROMENT.items():
            self.assertIsInstance(key,str)
            self.assertIsInstance(value,str)
    
    def test_containers(self):
        self.assertIsInstance(config.CONTAINERS,list)
        for container in config.CONTAINERS:
            self.assertIsInstance(container,str)
    
    def test_docker_compose_version(self):
        self.assertIsInstance(config.DOCKER_COMPOSE_VERSION,str)
    
    def test_network_name(self):
        self.assertIsInstance(config.NETWORK_NAME,str)
    
    def test_folder_to_save(self):
        self.assertIsInstance(config.FOLDER_TO_SAVE,str)
    
    def test_enable_https(self):
        self.assertIsInstance(config.ENABLE_HTTPS,bool)
    
    def test_server_names(self):
        self.assertIsInstance(config.SERVER_NAMES,list)
        for servername in config.SERVER_NAMES:
            self.assertIsInstance(servername,str)

    def test_number_web_instances(self):
        self.assertIsInstance(config.NUMBER_WEB_INSTANCES,int)


if __name__ == '__main__':
    unittest.main()