delete from privileges;
delete from resources;
delete from actions;
delete from controllers;
delete from users;
delete from roles;

---
--  Roles
---

insert into roles (id, name) values (1, 'administrator');
insert into roles (id, name) values (2, 'users');

---
--  Standard users
---

insert into users (username, password, role_id, email) values ('admin', 'sha256$l2ygbSdF$2d03f994b4d99fdf6ca30832852826564189f3438a9f6abc7249bc74c08b7843', 1, 'lucasssousa10@gmail.com');
insert into users (username, password, role_id, email) values ('user', 'sha256$l2ygbSdF$2d03f994b4d99fdf6ca30832852826564189f3438a9f6abc7249bc74c08b7843', 2, 'lucas.sousa@ppgcc.ifce.edu.br');

---
--  Controllers
---

insert into controllers (id, name) values (1, 'users');
insert into controllers (id, name) values (2, 'centroEstagio');	
insert into controllers (id, name) values (3, 'tipoEstudante');
insert into controllers (id, name) values (4, 'seguradora');
insert into controllers (id, name) values (5, 'empresa');
insert into controllers (id, name) values (6, 'contatoEmpresa');
insert into controllers (id, name) values (7, 'contratoEmpresa');
insert into controllers (id, name) values (8, 'cbo');
insert into controllers (id, name) values (9, 'experienciaProfissionalEstudante');
insert into controllers (id, name) values (10, 'estadoCivil');
insert into controllers (id, name) values (11, 'escola');
insert into controllers (id, name) values (12, 'tipoConhecimento');
insert into controllers (id, name) values (13, 'conhecimento');
insert into controllers (id, name) values (14, 'conhecimentoEstudante');
insert into controllers (id, name) values (15, 'periodoCurso');
insert into controllers (id, name) values (16, 'grauInstrucao');
insert into controllers (id, name) values (17, 'categoriaHabilitacao');
insert into controllers (id, name) values (18, 'tipoVeiculo');
insert into controllers (id, name) values (19, 'cursoAdicionalEstudante');
insert into controllers (id, name) values (20, 'cursoEstudante');
insert into controllers (id, name) values (21, 'estudante');
insert into controllers (id, name) values (22, 'cidade');
insert into controllers (id, name) values (23, 'uf');
insert into controllers (id, name) values (24, 'diasVaga');
insert into controllers (id, name) values (25, 'beneficio');
insert into controllers (id, name) values (26, 'beneficioVaga');
insert into controllers (id, name) values (27, 'vaga');
insert into controllers (id, name) values (28, 'convocacaoVaga');
insert into controllers (id, name) values (29, 'estudanteEncaminhado');
insert into controllers (id, name) values (30, 'roles');
insert into controllers (id, name) values (31, 'taxasTipoEstudante');
insert into controllers (id, name) values (32, 'apoliceMesAno');
insert into controllers (id, name) values (33, 'apoliceEstudante');
insert into controllers (id, name) values (34, 'apolice');



---
--  Actions
---

insert into actions (id, name) values (1, 'all');
insert into actions (id, name) values (2, 'view');
insert into actions (id, name) values (3, 'add');
insert into actions (id, name) values (4, 'edit');
insert into actions (id, name) values (5, 'delete');

---
--  Resources
---

insert into resources (id, controller_id, action_id) values (  1, 1, 1); -- users/all
insert into resources (id, controller_id, action_id) values (  2, 1, 2); -- users/view
insert into resources (id, controller_id, action_id) values (  3, 1, 3); -- users/add
insert into resources (id, controller_id, action_id) values (  4, 1, 4); -- users/edit
insert into resources (id, controller_id, action_id) values (  5, 1, 5); -- users/delete

insert into resources (id, controller_id, action_id) values (  6, 2, 1); -- centroEstagio/all
insert into resources (id, controller_id, action_id) values (  7, 2, 2); -- centroEstagio/view
insert into resources (id, controller_id, action_id) values (  8, 2, 3); -- centroEstagio/add
insert into resources (id, controller_id, action_id) values (  9, 2, 4); -- centroEstagio/edit
insert into resources (id, controller_id, action_id) values ( 10, 2, 5); -- centroEstagio/delete

insert into resources (id, controller_id, action_id) values ( 11, 3, 1); -- tipoEstudante/all
insert into resources (id, controller_id, action_id) values ( 12, 3, 2); -- tipoEstudante/view
insert into resources (id, controller_id, action_id) values ( 13, 3, 3); -- tipoEstudante/add
insert into resources (id, controller_id, action_id) values ( 14, 3, 4); -- tipoEstudante/edit
insert into resources (id, controller_id, action_id) values ( 15, 3, 5); -- tipoEstudante/delete

insert into resources (id, controller_id, action_id) values ( 16, 4, 1); -- seguradora/all
insert into resources (id, controller_id, action_id) values ( 17, 4, 2); -- seguradora/view
insert into resources (id, controller_id, action_id) values ( 18, 4, 3); -- seguradora/add
insert into resources (id, controller_id, action_id) values ( 19, 4, 4); -- seguradora/edit
insert into resources (id, controller_id, action_id) values ( 20, 4, 5); -- seguradora/delete

insert into resources (id, controller_id, action_id) values ( 21, 5, 1); -- empresa/all
insert into resources (id, controller_id, action_id) values ( 22, 5, 2); -- empresa/view
insert into resources (id, controller_id, action_id) values ( 23, 5, 3); -- empresa/add
insert into resources (id, controller_id, action_id) values ( 24, 5, 4); -- empresa/edit
insert into resources (id, controller_id, action_id) values ( 25, 5, 5); -- empresa/delete

insert into resources (id, controller_id, action_id) values ( 26, 6, 1); -- contatoEmpresa/all
insert into resources (id, controller_id, action_id) values ( 27, 6, 2); -- contatoEmpresa/view
insert into resources (id, controller_id, action_id) values ( 28, 6, 3); -- contatoEmpresa/add
insert into resources (id, controller_id, action_id) values ( 29, 6, 4); -- contatoEmpresa/edit
insert into resources (id, controller_id, action_id) values ( 30, 6, 5); -- contatoEmpresa/delete

insert into resources (id, controller_id, action_id) values ( 31, 7, 1); -- contratoEmpresa/all
insert into resources (id, controller_id, action_id) values ( 32, 7, 2); -- contratoEmpresa/view
insert into resources (id, controller_id, action_id) values ( 33, 7, 3); -- contratoEmpresa/add
insert into resources (id, controller_id, action_id) values ( 34, 7, 4); -- contratoEmpresa/edit
insert into resources (id, controller_id, action_id) values ( 35, 7, 5); -- contratoEmpresa/delete

insert into resources (id, controller_id, action_id) values (  36, 8, 1); -- cbo/all
insert into resources (id, controller_id, action_id) values (  37, 8, 2); -- cbo/view
insert into resources (id, controller_id, action_id) values (  38, 8, 3); -- cbo/add
insert into resources (id, controller_id, action_id) values (  39, 8, 4); -- cbo/edit
insert into resources (id, controller_id, action_id) values (  40, 8, 5); -- cbo/delete

insert into resources (id, controller_id, action_id) values (  41, 9, 1); -- experienciaProfissionalEstudante/all
insert into resources (id, controller_id, action_id) values (  42, 9, 2); -- experienciaProfissionalEstudante/view
insert into resources (id, controller_id, action_id) values (  43, 9, 3); -- experienciaProfissionalEstudante/add
insert into resources (id, controller_id, action_id) values (  44, 9, 4); -- experienciaProfissionalEstudante/edit
insert into resources (id, controller_id, action_id) values (  45, 9, 5); -- experienciaProfissionalEstudante/delete

insert into resources (id, controller_id, action_id) values (  46, 10, 1); -- estadoCivil/all
insert into resources (id, controller_id, action_id) values (  47, 10, 2); -- estadoCivil/view
insert into resources (id, controller_id, action_id) values (  48, 10, 3); -- estadoCivil/add
insert into resources (id, controller_id, action_id) values (  49, 10, 4); -- estadoCivil/edit
insert into resources (id, controller_id, action_id) values (  50, 10, 5); -- estadoCivil/delete

insert into resources (id, controller_id, action_id) values (  51, 11, 1); -- escola/all
insert into resources (id, controller_id, action_id) values (  52, 11, 2); -- escola/view
insert into resources (id, controller_id, action_id) values (  53, 11, 3); -- escola/add
insert into resources (id, controller_id, action_id) values (  54, 11, 4); -- escola/edit
insert into resources (id, controller_id, action_id) values (  55, 11, 5); -- escola/delete

insert into resources (id, controller_id, action_id) values (  56, 12, 1); -- tipoConhecimento/all
insert into resources (id, controller_id, action_id) values (  57, 12, 2); -- tipoConhecimento/view
insert into resources (id, controller_id, action_id) values (  58, 12, 3); -- tipoConhecimento/add
insert into resources (id, controller_id, action_id) values (  59, 12, 4); -- tipoConhecimento/edit
insert into resources (id, controller_id, action_id) values (  60, 12, 5); -- tipoConhecimento/delete

insert into resources (id, controller_id, action_id) values (  61, 13, 1); -- conhecimento/all
insert into resources (id, controller_id, action_id) values (  62, 13, 2); -- conhecimento/view
insert into resources (id, controller_id, action_id) values (  63, 13, 3); -- conhecimento/add
insert into resources (id, controller_id, action_id) values (  64, 13, 4); -- conhecimento/edit
insert into resources (id, controller_id, action_id) values (  65, 13, 5); -- conhecimento/delete

insert into resources (id, controller_id, action_id) values (  66, 14, 1); -- conhecimentoEstudante/all
insert into resources (id, controller_id, action_id) values (  67, 14, 2); -- conhecimentoEstudante/view
insert into resources (id, controller_id, action_id) values (  68, 14, 3); -- conhecimentoEstudante/add
insert into resources (id, controller_id, action_id) values (  69, 14, 4); -- conhecimentoEstudante/edit
insert into resources (id, controller_id, action_id) values (  70, 14, 5); -- conhecimentoEstudante/delete

insert into resources (id, controller_id, action_id) values (  71, 15, 1); -- periodoCurso/all
insert into resources (id, controller_id, action_id) values (  72, 15, 2); -- periodoCurso/view
insert into resources (id, controller_id, action_id) values (  73, 15, 3); -- periodoCurso/add
insert into resources (id, controller_id, action_id) values (  74, 15, 4); -- periodoCurso/edit
insert into resources (id, controller_id, action_id) values (  75, 15, 5); -- periodoCurso/delete

insert into resources (id, controller_id, action_id) values (  76, 16, 1); -- grauInstrucao/all
insert into resources (id, controller_id, action_id) values (  77, 16, 2); -- grauInstrucao/view
insert into resources (id, controller_id, action_id) values (  78, 16, 3); -- grauInstrucao/add
insert into resources (id, controller_id, action_id) values (  79, 16, 4); -- grauInstrucao/edit
insert into resources (id, controller_id, action_id) values (  80, 16, 5); -- grauInstrucao/delete

insert into resources (id, controller_id, action_id) values (  81, 17, 1); -- categoriaHabilitacao/all
insert into resources (id, controller_id, action_id) values (  82, 17, 2); -- categoriaHabilitacao/view
insert into resources (id, controller_id, action_id) values (  83, 17, 3); -- categoriaHabilitacao/add
insert into resources (id, controller_id, action_id) values (  84, 17, 4); -- categoriaHabilitacao/edit
insert into resources (id, controller_id, action_id) values (  85, 17, 5); -- categoriaHabilitacao/delete

insert into resources (id, controller_id, action_id) values (  86, 18, 1); -- tipoVeiculo/all
insert into resources (id, controller_id, action_id) values (  87, 18, 2); -- tipoVeiculo/view
insert into resources (id, controller_id, action_id) values (  88, 18, 3); -- tipoVeiculo/add
insert into resources (id, controller_id, action_id) values (  89, 18, 4); -- tipoVeiculo/edit
insert into resources (id, controller_id, action_id) values (  90, 18, 5); -- tipoVeiculo/delete

insert into resources (id, controller_id, action_id) values (  91, 19, 1); -- cursoAdicionalEstudante/all
insert into resources (id, controller_id, action_id) values (  92, 19, 2); -- cursoAdicionalEstudante/view
insert into resources (id, controller_id, action_id) values (  93, 19, 3); -- cursoAdicionalEstudante/add
insert into resources (id, controller_id, action_id) values (  94, 19, 4); -- cursoAdicionalEstudante/edit
insert into resources (id, controller_id, action_id) values (  95, 19, 5); -- cursoAdicionalEstudante/delete

insert into resources (id, controller_id, action_id) values (  96, 20, 1); -- cursoEstudante/all
insert into resources (id, controller_id, action_id) values (  97, 20, 2); -- cursoEstudante/view
insert into resources (id, controller_id, action_id) values (  98, 20, 3); -- cursoEstudante/add
insert into resources (id, controller_id, action_id) values (  99, 20, 4); -- cursoEstudante/edit
insert into resources (id, controller_id, action_id) values (  100, 20, 5); -- cursoEstudante/delete

insert into resources (id, controller_id, action_id) values (  101, 21, 1); -- estudante/all
insert into resources (id, controller_id, action_id) values (  102, 21, 2); -- estudante/view
insert into resources (id, controller_id, action_id) values (  103, 21, 3); -- estudante/add
insert into resources (id, controller_id, action_id) values (  104, 21, 4); -- estudante/edit
insert into resources (id, controller_id, action_id) values (  105, 21, 5); -- estudante/delete

insert into resources (id, controller_id, action_id) values (  106, 22, 1); -- cidade/all
insert into resources (id, controller_id, action_id) values (  107, 22, 2); -- cidade/view
insert into resources (id, controller_id, action_id) values (  108, 22, 3); -- cidade/add
insert into resources (id, controller_id, action_id) values (  109, 22, 4); -- cidade/edit
insert into resources (id, controller_id, action_id) values (  110, 22, 5); -- cidade/delete

insert into resources (id, controller_id, action_id) values (  111, 23, 1); -- uf/all
insert into resources (id, controller_id, action_id) values (  112, 23, 2); -- uf/view
insert into resources (id, controller_id, action_id) values (  113, 23, 3); -- uf/add
insert into resources (id, controller_id, action_id) values (  114, 23, 4); -- uf/edit
insert into resources (id, controller_id, action_id) values (  115, 23, 5); -- uf/delete


insert into resources (id, controller_id, action_id) values (  116, 24, 1); -- diasVaga/all
insert into resources (id, controller_id, action_id) values (  117, 24, 2); -- diasVaga/view
insert into resources (id, controller_id, action_id) values (  118, 24, 3); -- diasVaga/add
insert into resources (id, controller_id, action_id) values (  119, 24, 4); -- diasVaga/edit
insert into resources (id, controller_id, action_id) values (  120, 24, 5); -- diasVaga/delete

insert into resources (id, controller_id, action_id) values (  121, 25, 1); -- beneficio/all
insert into resources (id, controller_id, action_id) values (  122, 25, 2); -- beneficio/view
insert into resources (id, controller_id, action_id) values (  123, 25, 3); -- beneficio/add
insert into resources (id, controller_id, action_id) values (  124, 25, 4); -- beneficio/edit
insert into resources (id, controller_id, action_id) values (  125, 25, 5); -- beneficio/delete

insert into resources (id, controller_id, action_id) values (  126, 26, 1); -- beneficioVaga/all
insert into resources (id, controller_id, action_id) values (  127, 26, 2); -- beneficioVaga/view
insert into resources (id, controller_id, action_id) values (  128, 26, 3); -- beneficioVaga/add
insert into resources (id, controller_id, action_id) values (  129, 26, 4); -- beneficioVaga/edit
insert into resources (id, controller_id, action_id) values (  130, 26, 5); -- beneficioVaga/delete

insert into resources (id, controller_id, action_id) values (  131, 27, 1); -- vaga/all
insert into resources (id, controller_id, action_id) values (  132, 27, 2); -- vaga/view
insert into resources (id, controller_id, action_id) values (  133, 27, 3); -- vaga/add
insert into resources (id, controller_id, action_id) values (  134, 27, 4); -- vaga/edit
insert into resources (id, controller_id, action_id) values (  135, 27, 5); -- vaga/delete

insert into resources (id, controller_id, action_id) values (  136, 28, 1); -- convocacaoVaga/all
insert into resources (id, controller_id, action_id) values (  137, 28, 2); -- convocacaoVaga/view
insert into resources (id, controller_id, action_id) values (  138, 28, 3); -- convocacaoVaga/add
insert into resources (id, controller_id, action_id) values (  139, 28, 4); -- convocacaoVaga/edit
insert into resources (id, controller_id, action_id) values (  140, 28, 5); -- convocacaoVaga/delete

insert into resources (id, controller_id, action_id) values (  141, 29, 1); -- estudanteEncaminhado/all
insert into resources (id, controller_id, action_id) values (  142, 29, 2); -- estudanteEncaminhado/view
insert into resources (id, controller_id, action_id) values (  143, 29, 3); -- estudanteEncaminhado/add
insert into resources (id, controller_id, action_id) values (  144, 29, 4); -- estudanteEncaminhado/edit
insert into resources (id, controller_id, action_id) values (  145, 29, 5); -- estudanteEncaminhado/delete

insert into resources (id, controller_id, action_id) values (  146, 30, 1); -- roles/all
insert into resources (id, controller_id, action_id) values (  147, 30, 2); -- roles/view
insert into resources (id, controller_id, action_id) values (  148, 30, 3); -- roles/add
insert into resources (id, controller_id, action_id) values (  149, 30, 4); -- roles/edit
insert into resources (id, controller_id, action_id) values (  150, 30, 5); -- roles/delete

insert into resources (id, controller_id, action_id) values (  151, 31, 1); -- taxasTipoEstudante/all
insert into resources (id, controller_id, action_id) values (  152, 31, 2); -- taxasTipoEstudante/view
insert into resources (id, controller_id, action_id) values (  153, 31, 3); -- taxasTipoEstudante/add
insert into resources (id, controller_id, action_id) values (  154, 31, 4); -- taxasTipoEstudante/edit
insert into resources (id, controller_id, action_id) values (  155, 31, 5); -- taxasTipoEstudante/delete

insert into resources (id, controller_id, action_id) values (  156, 32, 1); -- apoliceMesAno/all
insert into resources (id, controller_id, action_id) values (  157, 32, 2); -- apoliceMesAno/view
insert into resources (id, controller_id, action_id) values (  158, 32, 3); -- apoliceMesAno/add
insert into resources (id, controller_id, action_id) values (  159, 32, 4); -- apoliceMesAno/edit
insert into resources (id, controller_id, action_id) values (  160, 32, 5); -- apoliceMesAno/delete

insert into resources (id, controller_id, action_id) values (  161, 33, 1); -- apoliceEstudante/all
insert into resources (id, controller_id, action_id) values (  162, 33, 2); -- apoliceEstudante/view
insert into resources (id, controller_id, action_id) values (  163, 33, 3); -- apoliceEstudante/add
insert into resources (id, controller_id, action_id) values (  164, 33, 4); -- apoliceEstudante/edit
insert into resources (id, controller_id, action_id) values (  165, 33, 5); -- apoliceEstudante/delete

insert into resources (id, controller_id, action_id) values (  166, 34, 1); -- apolice/all
insert into resources (id, controller_id, action_id) values (  167, 34, 2); -- apolice/view
insert into resources (id, controller_id, action_id) values (  168, 34, 3); -- apolice/add
insert into resources (id, controller_id, action_id) values (  169, 34, 4); -- apolice/edit
insert into resources (id, controller_id, action_id) values (  170, 34, 5); -- apolice/delete

---
--  Privileges
---

-- administrator

insert into privileges (role_id, resource_id, allow) values (1,  1, true); -- users/all
insert into privileges (role_id, resource_id, allow) values (1,  2, true); -- users/view
insert into privileges (role_id, resource_id, allow) values (1,  3, true); -- users/add
insert into privileges (role_id, resource_id, allow) values (1,  4, true); -- users/edit
insert into privileges (role_id, resource_id, allow) values (1,  5, true); -- users/delete

insert into privileges (role_id, resource_id, allow) values (1,  6, true); -- centroEstagio/all
insert into privileges (role_id, resource_id, allow) values (1,  7, true); -- centroEstagio/view
insert into privileges (role_id, resource_id, allow) values (1,  8, true); -- centroEstagio/add
insert into privileges (role_id, resource_id, allow) values (1,  9, true); -- centroEstagio/edit
insert into privileges (role_id, resource_id, allow) values (1, 10, true); -- centroEstagio/delete

insert into privileges (role_id, resource_id, allow) values (1, 11, true); -- tipoEstudante/all
insert into privileges (role_id, resource_id, allow) values (1, 12, true); -- tipoEstudante/view
insert into privileges (role_id, resource_id, allow) values (1, 13, true); -- tipoEstudante/add
insert into privileges (role_id, resource_id, allow) values (1, 14, true); -- tipoEstudante/edit
insert into privileges (role_id, resource_id, allow) values (1, 15, true); -- tipoEstudante/delete

insert into privileges (role_id, resource_id, allow) values (1, 16, true); -- seguradora/all
insert into privileges (role_id, resource_id, allow) values (1, 17, true); -- seguradora/view
insert into privileges (role_id, resource_id, allow) values (1, 18, true); -- seguradora/add
insert into privileges (role_id, resource_id, allow) values (1, 19, true); -- seguradora/edit
insert into privileges (role_id, resource_id, allow) values (1, 20, true); -- seguradora/delete

insert into privileges (role_id, resource_id, allow) values (1, 21, true); -- empresa/all
insert into privileges (role_id, resource_id, allow) values (1, 22, true); -- empresa/view
insert into privileges (role_id, resource_id, allow) values (1, 23, true); -- empresa/add
insert into privileges (role_id, resource_id, allow) values (1, 24, true); -- empresa/edit
insert into privileges (role_id, resource_id, allow) values (1, 25, true); -- empresa/delete

insert into privileges (role_id, resource_id, allow) values (1, 26, true); -- contatoEmpresa/all
insert into privileges (role_id, resource_id, allow) values (1, 27, true); -- contatoEmpresa/view
insert into privileges (role_id, resource_id, allow) values (1, 28, true); -- contatoEmpresa/add
insert into privileges (role_id, resource_id, allow) values (1, 29, true); -- contatoEmpresa/edit
insert into privileges (role_id, resource_id, allow) values (1, 30, true); -- contatoEmpresa/delete

insert into privileges (role_id, resource_id, allow) values (1, 31, true); -- contratoEmpresa/all
insert into privileges (role_id, resource_id, allow) values (1, 32, true); -- contratoEmpresa/view
insert into privileges (role_id, resource_id, allow) values (1, 33, true); -- contratoEmpresa/add
insert into privileges (role_id, resource_id, allow) values (1, 34, true); -- contratoEmpresa/edit
insert into privileges (role_id, resource_id, allow) values (1, 35, true); -- contratoEmpresa/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  36, true); -- cbo/all
insert into privileges (role_id, resource_id, allow) values ( 1,  37, true); -- cbo/view
insert into privileges (role_id, resource_id, allow) values ( 1,  38, true); -- cbo/add
insert into privileges (role_id, resource_id, allow) values ( 1,  39, true); -- cbo/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  40, true); -- cbo/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  41, true); -- experienciaProfissionalEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 1,  42, true); -- experienciaProfissionalEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 1,  43, true); -- experienciaProfissionalEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 1,  44, true); -- experienciaProfissionalEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  45, true); -- experienciaProfissionalEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  46, true); -- estadoCivil/all
insert into privileges (role_id, resource_id, allow) values ( 1,  47, true); -- estadoCivil/view
insert into privileges (role_id, resource_id, allow) values ( 1,  48, true); -- estadoCivil/add
insert into privileges (role_id, resource_id, allow) values ( 1,  49, true); -- estadoCivil/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  50, true); -- estadoCivil/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  51, true); -- escola/all
insert into privileges (role_id, resource_id, allow) values ( 1,  52, true); -- escola/view
insert into privileges (role_id, resource_id, allow) values ( 1,  53, true); -- escola/add
insert into privileges (role_id, resource_id, allow) values ( 1,  54, true); -- escola/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  55, true); -- escola/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  56, true); -- tipoConhecimento/all
insert into privileges (role_id, resource_id, allow) values ( 1,  57, true); -- tipoConhecimento/view
insert into privileges (role_id, resource_id, allow) values ( 1,  58, true); -- tipoConhecimento/add
insert into privileges (role_id, resource_id, allow) values ( 1,  59, true); -- tipoConhecimento/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  60, true); -- tipoConhecimento/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  61, true); -- conhecimento/all
insert into privileges (role_id, resource_id, allow) values ( 1,  62, true); -- conhecimento/view
insert into privileges (role_id, resource_id, allow) values ( 1,  63, true); -- conhecimento/add
insert into privileges (role_id, resource_id, allow) values ( 1,  64, true); -- conhecimento/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  65, true); -- conhecimento/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  66, true); -- conhecimentoEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 1,  67, true); -- conhecimentoEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 1,  68, true); -- conhecimentoEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 1,  69, true); -- conhecimentoEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  70, true); -- conhecimentoEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  71, true); -- periodoCurso/all
insert into privileges (role_id, resource_id, allow) values ( 1,  72, true); -- periodoCurso/view
insert into privileges (role_id, resource_id, allow) values ( 1,  73, true); -- periodoCurso/add
insert into privileges (role_id, resource_id, allow) values ( 1,  74, true); -- periodoCurso/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  75, true); -- periodoCurso/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  76, true); -- grauInstrucao/all
insert into privileges (role_id, resource_id, allow) values ( 1,  77, true); -- grauInstrucao/view
insert into privileges (role_id, resource_id, allow) values ( 1,  78, true); -- grauInstrucao/add
insert into privileges (role_id, resource_id, allow) values ( 1,  79, true); -- grauInstrucao/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  80, true); -- grauInstrucao/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  81, true); -- categoriaHabilitacao/all
insert into privileges (role_id, resource_id, allow) values ( 1,  82, true); -- categoriaHabilitacao/view
insert into privileges (role_id, resource_id, allow) values ( 1,  83, true); -- categoriaHabilitacao/add
insert into privileges (role_id, resource_id, allow) values ( 1,  84, true); -- categoriaHabilitacao/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  85, true); -- categoriaHabilitacao/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  86, true); -- tipoVeiculo/all
insert into privileges (role_id, resource_id, allow) values ( 1,  87, true); -- tipoVeiculo/view
insert into privileges (role_id, resource_id, allow) values ( 1,  88, true); -- tipoVeiculo/add
insert into privileges (role_id, resource_id, allow) values ( 1,  89, true); -- tipoVeiculo/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  90, true); -- tipoVeiculo/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  91, true); -- cursoAdicionalEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 1,  92, true); -- cursoAdicionalEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 1,  93, true); -- cursoAdicionalEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 1,  94, true); -- cursoAdicionalEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  95, true); -- cursoAdicionalEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  96, true); -- cursoEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 1,  97, true); -- cursoEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 1,  98, true); -- cursoEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 1,  99, true); -- cursoEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  100, true); -- cursoEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  101, true); -- estudante/all
insert into privileges (role_id, resource_id, allow) values ( 1,  102, true); -- estudante/view
insert into privileges (role_id, resource_id, allow) values ( 1,  103, true); -- estudante/add
insert into privileges (role_id, resource_id, allow) values ( 1,  104, true); -- estudante/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  105, true); -- estudante/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  106, true); -- cidade/all
insert into privileges (role_id, resource_id, allow) values ( 1,  107, true); -- cidade/view
insert into privileges (role_id, resource_id, allow) values ( 1,  108, true); -- cidade/add
insert into privileges (role_id, resource_id, allow) values ( 1,  109, true); -- cidade/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  110, true); -- cidade/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  111, true); -- uf/all
insert into privileges (role_id, resource_id, allow) values ( 1,  112, true); -- uf/view
insert into privileges (role_id, resource_id, allow) values ( 1,  113, true); -- uf/add
insert into privileges (role_id, resource_id, allow) values ( 1,  114, true); -- uf/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  115, true); -- uf/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  116, true); -- diasVaga/all
insert into privileges (role_id, resource_id, allow) values ( 1,  117, true); -- diasVaga/view
insert into privileges (role_id, resource_id, allow) values ( 1,  118, true); -- diasVaga/add
insert into privileges (role_id, resource_id, allow) values ( 1,  119, true); -- diasVaga/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  120, true); -- diasVaga/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  121, true); -- beneficio/all
insert into privileges (role_id, resource_id, allow) values ( 1,  122, true); -- beneficio/view
insert into privileges (role_id, resource_id, allow) values ( 1,  123, true); -- beneficio/add
insert into privileges (role_id, resource_id, allow) values ( 1,  124, true); -- beneficio/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  125, true); -- beneficio/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  126, true); -- beneficioVaga/all
insert into privileges (role_id, resource_id, allow) values ( 1,  127, true); -- beneficioVaga/view
insert into privileges (role_id, resource_id, allow) values ( 1,  128, true); -- beneficioVaga/add
insert into privileges (role_id, resource_id, allow) values ( 1,  129, true); -- beneficioVaga/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  130, true); -- beneficioVaga/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  131, true); -- vaga/all
insert into privileges (role_id, resource_id, allow) values ( 1,  132, true); -- vaga/view
insert into privileges (role_id, resource_id, allow) values ( 1,  133, true); -- vaga/add
insert into privileges (role_id, resource_id, allow) values ( 1,  134, true); -- vaga/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  135, true); -- vaga/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  136, true); -- convocacaoVaga/all
insert into privileges (role_id, resource_id, allow) values ( 1,  137, true); -- convocacaoVaga/view
insert into privileges (role_id, resource_id, allow) values ( 1,  138, true); -- convocacaoVaga/add
insert into privileges (role_id, resource_id, allow) values ( 1,  139, true); -- convocacaoVaga/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  140, true); -- convocacaoVaga/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  141, true); -- estudanteEncaminhado/all
insert into privileges (role_id, resource_id, allow) values ( 1,  142, true); -- estudanteEncaminhado/view
insert into privileges (role_id, resource_id, allow) values ( 1,  143, true); -- estudanteEncaminhado/add
insert into privileges (role_id, resource_id, allow) values ( 1,  144, true); -- estudanteEncaminhado/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  145, true); -- estudanteEncaminhado/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  146, true); -- roles/all
insert into privileges (role_id, resource_id, allow) values ( 1,  147, true); -- roles/view
insert into privileges (role_id, resource_id, allow) values ( 1,  148, true); -- roles/add
insert into privileges (role_id, resource_id, allow) values ( 1,  149, true); -- roles/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  150, true); -- roles/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  151, true); -- taxasTipoEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 1,  152, true); -- taxasTipoEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 1,  153, true); -- taxasTipoEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 1,  154, true); -- taxasTipoEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  155, true); -- taxasTipoEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  156, true); -- apoliceMesAno/all
insert into privileges (role_id, resource_id, allow) values ( 1,  157, true); -- apoliceMesAno/view
insert into privileges (role_id, resource_id, allow) values ( 1,  158, true); -- apoliceMesAno/add
insert into privileges (role_id, resource_id, allow) values ( 1,  159, true); -- apoliceMesAno/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  160, true); -- apoliceMesAno/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  161, true); -- apoliceEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 1,  162, true); -- apoliceEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 1,  163, true); -- apoliceEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 1,  164, true); -- apoliceEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  165, true); -- apoliceEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 1,  166, true); -- apolice/all
insert into privileges (role_id, resource_id, allow) values ( 1,  167, true); -- apolice/view
insert into privileges (role_id, resource_id, allow) values ( 1,  168, true); -- apolice/add
insert into privileges (role_id, resource_id, allow) values ( 1,  169, true); -- apolice/edit
insert into privileges (role_id, resource_id, allow) values ( 1,  170, true); -- apolice/delete


-- users

insert into privileges (role_id, resource_id, allow) values (2, 1, false); -- users/all
insert into privileges (role_id, resource_id, allow) values (2, 2, false); -- users/view
insert into privileges (role_id, resource_id, allow) values (2, 3, false); -- users/add
insert into privileges (role_id, resource_id, allow) values (2, 4, false); -- users/edit
insert into privileges (role_id, resource_id, allow) values (2, 5, false); -- users/delete

insert into privileges (role_id, resource_id, allow) values (2,  6, true); -- centroEstagio/all
insert into privileges (role_id, resource_id, allow) values (2,  7, true); -- centroEstagio/view
insert into privileges (role_id, resource_id, allow) values (2,  8, true); -- centroEstagio/add
insert into privileges (role_id, resource_id, allow) values (2,  9, true); -- centroEstagio/edit
insert into privileges (role_id, resource_id, allow) values (2, 10, true); -- centroEstagio/delete

insert into privileges (role_id, resource_id, allow) values (2, 11, true); -- tipoEstudante/all
insert into privileges (role_id, resource_id, allow) values (2, 12, true); -- tipoEstudante/view
insert into privileges (role_id, resource_id, allow) values (2, 13, true); -- tipoEstudante/add
insert into privileges (role_id, resource_id, allow) values (2, 14, true); -- tipoEstudante/edit
insert into privileges (role_id, resource_id, allow) values (2, 15, true); -- tipoEstudante/delete

insert into privileges (role_id, resource_id, allow) values (2, 16, true); -- seguradora/all
insert into privileges (role_id, resource_id, allow) values (2, 17, true); -- seguradora/view
insert into privileges (role_id, resource_id, allow) values (2, 18, true); -- seguradora/add
insert into privileges (role_id, resource_id, allow) values (2, 19, true); -- seguradora/edit
insert into privileges (role_id, resource_id, allow) values (2, 20, true); -- seguradora/delete

insert into privileges (role_id, resource_id, allow) values (2, 21, true); -- empresa/all
insert into privileges (role_id, resource_id, allow) values (2, 22, true); -- empresa/view
insert into privileges (role_id, resource_id, allow) values (2, 23, true); -- empresa/add
insert into privileges (role_id, resource_id, allow) values (2, 24, true); -- empresa/edit
insert into privileges (role_id, resource_id, allow) values (2, 25, true); -- empresa/delete

insert into privileges (role_id, resource_id, allow) values (2, 26, true); -- contatoEmpresa/all
insert into privileges (role_id, resource_id, allow) values (2, 27, true); -- contatoEmpresa/view
insert into privileges (role_id, resource_id, allow) values (2, 28, true); -- contatoEmpresa/add
insert into privileges (role_id, resource_id, allow) values (2, 29, true); -- contatoEmpresa/edit
insert into privileges (role_id, resource_id, allow) values (2, 30, true); -- contatoEmpresa/delete

insert into privileges (role_id, resource_id, allow) values (2, 31, true); -- contratoEmpresa/all
insert into privileges (role_id, resource_id, allow) values (2, 32, true); -- contratoEmpresa/view
insert into privileges (role_id, resource_id, allow) values (2, 33, true); -- contratoEmpresa/add
insert into privileges (role_id, resource_id, allow) values (2, 34, true); -- contratoEmpresa/edit
insert into privileges (role_id, resource_id, allow) values (2, 35, true); -- contratoEmpresa/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  36, true); -- cbo/all
insert into privileges (role_id, resource_id, allow) values ( 2,  37, true); -- cbo/view
insert into privileges (role_id, resource_id, allow) values ( 2,  38, true); -- cbo/add
insert into privileges (role_id, resource_id, allow) values ( 2,  39, true); -- cbo/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  40, true); -- cbo/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  41, true); -- experienciaProfissionalEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 2,  42, true); -- experienciaProfissionalEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 2,  43, true); -- experienciaProfissionalEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 2,  44, true); -- experienciaProfissionalEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  45, true); -- experienciaProfissionalEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  46, true); -- estadoCivil/all
insert into privileges (role_id, resource_id, allow) values ( 2,  47, true); -- estadoCivil/view
insert into privileges (role_id, resource_id, allow) values ( 2,  48, true); -- estadoCivil/add
insert into privileges (role_id, resource_id, allow) values ( 2,  49, true); -- estadoCivil/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  50, true); -- estadoCivil/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  51, true); -- escola/all
insert into privileges (role_id, resource_id, allow) values ( 2,  52, true); -- escola/view
insert into privileges (role_id, resource_id, allow) values ( 2,  53, true); -- escola/add
insert into privileges (role_id, resource_id, allow) values ( 2,  54, true); -- escola/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  55, true); -- escola/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  56, true); -- tipoConhecimento/all
insert into privileges (role_id, resource_id, allow) values ( 2,  57, true); -- tipoConhecimento/view
insert into privileges (role_id, resource_id, allow) values ( 2,  58, true); -- tipoConhecimento/add
insert into privileges (role_id, resource_id, allow) values ( 2,  59, true); -- tipoConhecimento/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  60, true); -- tipoConhecimento/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  61, true); -- conhecimento/all
insert into privileges (role_id, resource_id, allow) values ( 2,  62, true); -- conhecimento/view
insert into privileges (role_id, resource_id, allow) values ( 2,  63, true); -- conhecimento/add
insert into privileges (role_id, resource_id, allow) values ( 2,  64, true); -- conhecimento/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  65, true); -- conhecimento/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  66, true); -- conhecimentoEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 2,  67, true); -- conhecimentoEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 2,  68, true); -- conhecimentoEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 2,  69, true); -- conhecimentoEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  70, true); -- conhecimentoEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  71, true); -- periodoCurso/all
insert into privileges (role_id, resource_id, allow) values ( 2,  72, true); -- periodoCurso/view
insert into privileges (role_id, resource_id, allow) values ( 2,  73, true); -- periodoCurso/add
insert into privileges (role_id, resource_id, allow) values ( 2,  74, true); -- periodoCurso/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  75, true); -- periodoCurso/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  76, true); -- grauInstrucao/all
insert into privileges (role_id, resource_id, allow) values ( 2,  77, true); -- grauInstrucao/view
insert into privileges (role_id, resource_id, allow) values ( 2,  78, true); -- grauInstrucao/add
insert into privileges (role_id, resource_id, allow) values ( 2,  79, true); -- grauInstrucao/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  80, true); -- grauInstrucao/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  81, true); -- categoriaHabilitacao/all
insert into privileges (role_id, resource_id, allow) values ( 2,  82, true); -- categoriaHabilitacao/view
insert into privileges (role_id, resource_id, allow) values ( 2,  83, true); -- categoriaHabilitacao/add
insert into privileges (role_id, resource_id, allow) values ( 2,  84, true); -- categoriaHabilitacao/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  85, true); -- categoriaHabilitacao/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  86, true); -- tipoVeiculo/all
insert into privileges (role_id, resource_id, allow) values ( 2,  87, true); -- tipoVeiculo/view
insert into privileges (role_id, resource_id, allow) values ( 2,  88, true); -- tipoVeiculo/add
insert into privileges (role_id, resource_id, allow) values ( 2,  89, true); -- tipoVeiculo/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  90, true); -- tipoVeiculo/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  91, true); -- cursoAdicionalEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 2,  92, true); -- cursoAdicionalEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 2,  93, true); -- cursoAdicionalEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 2,  94, true); -- cursoAdicionalEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  95, true); -- cursoAdicionalEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  96, true); -- cursoEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 2,  97, true); -- cursoEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 2,  98, true); -- cursoEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 2,  99, true); -- cursoEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  100, true); -- cursoEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  101, true); -- estudante/all
insert into privileges (role_id, resource_id, allow) values ( 2,  102, true); -- estudante/view
insert into privileges (role_id, resource_id, allow) values ( 2,  103, true); -- estudante/add
insert into privileges (role_id, resource_id, allow) values ( 2,  104, true); -- estudante/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  105, true); -- estudante/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  106, true); -- cidade/all
insert into privileges (role_id, resource_id, allow) values ( 2,  107, true); -- cidade/view
insert into privileges (role_id, resource_id, allow) values ( 2,  108, true); -- cidade/add
insert into privileges (role_id, resource_id, allow) values ( 2,  109, true); -- cidade/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  110, true); -- cidade/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  111, true); -- uf/all
insert into privileges (role_id, resource_id, allow) values ( 2,  112, true); -- uf/view
insert into privileges (role_id, resource_id, allow) values ( 2,  113, true); -- uf/add
insert into privileges (role_id, resource_id, allow) values ( 2,  114, true); -- uf/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  115, true); -- uf/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  116, true); -- diasVaga/all
insert into privileges (role_id, resource_id, allow) values ( 2,  117, true); -- diasVaga/view
insert into privileges (role_id, resource_id, allow) values ( 2,  118, true); -- diasVaga/add
insert into privileges (role_id, resource_id, allow) values ( 2,  119, true); -- diasVaga/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  120, true); -- diasVaga/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  121, true); -- beneficio/all
insert into privileges (role_id, resource_id, allow) values ( 2,  122, true); -- beneficio/view
insert into privileges (role_id, resource_id, allow) values ( 2,  123, true); -- beneficio/add
insert into privileges (role_id, resource_id, allow) values ( 2,  124, true); -- beneficio/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  125, true); -- beneficio/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  126, true); -- beneficioVaga/all
insert into privileges (role_id, resource_id, allow) values ( 2,  127, true); -- beneficioVaga/view
insert into privileges (role_id, resource_id, allow) values ( 2,  128, true); -- beneficioVaga/add
insert into privileges (role_id, resource_id, allow) values ( 2,  129, true); -- beneficioVaga/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  130, true); -- beneficioVaga/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  131, true); -- vaga/all
insert into privileges (role_id, resource_id, allow) values ( 2,  132, true); -- vaga/view
insert into privileges (role_id, resource_id, allow) values ( 2,  133, true); -- vaga/add
insert into privileges (role_id, resource_id, allow) values ( 2,  134, true); -- vaga/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  135, true); -- vaga/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  136, true); -- convocacaoVaga/all
insert into privileges (role_id, resource_id, allow) values ( 2,  137, true); -- convocacaoVaga/view
insert into privileges (role_id, resource_id, allow) values ( 2,  138, true); -- convocacaoVaga/add
insert into privileges (role_id, resource_id, allow) values ( 2,  139, true); -- convocacaoVaga/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  140, true); -- convocacaoVaga/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  141, true); -- estudanteEncaminhado/all
insert into privileges (role_id, resource_id, allow) values ( 2,  142, true); -- estudanteEncaminhado/view
insert into privileges (role_id, resource_id, allow) values ( 2,  143, true); -- estudanteEncaminhado/add
insert into privileges (role_id, resource_id, allow) values ( 2,  144, true); -- estudanteEncaminhado/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  145, true); -- estudanteEncaminhado/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  146, true); -- roles/all
insert into privileges (role_id, resource_id, allow) values ( 2,  147, true); -- roles/view
insert into privileges (role_id, resource_id, allow) values ( 2,  148, true); -- roles/add
insert into privileges (role_id, resource_id, allow) values ( 2,  149, true); -- roles/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  150, true); -- roles/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  151, true); -- taxasTipoEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 2,  152, true); -- taxasTipoEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 2,  153, true); -- taxasTipoEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 2,  154, true); -- taxasTipoEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  155, true); -- taxasTipoEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  156, true); -- apoliceMesAno/all
insert into privileges (role_id, resource_id, allow) values ( 2,  157, true); -- apoliceMesAno/view
insert into privileges (role_id, resource_id, allow) values ( 2,  158, true); -- apoliceMesAno/add
insert into privileges (role_id, resource_id, allow) values ( 2,  159, true); -- apoliceMesAno/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  160, true); -- apoliceMesAno/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  161, true); -- apoliceEstudante/all
insert into privileges (role_id, resource_id, allow) values ( 2,  162, true); -- apoliceEstudante/view
insert into privileges (role_id, resource_id, allow) values ( 2,  163, true); -- apoliceEstudante/add
insert into privileges (role_id, resource_id, allow) values ( 2,  164, true); -- apoliceEstudante/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  165, true); -- apoliceEstudante/delete

insert into privileges (role_id, resource_id, allow) values ( 2,  166, true); -- apolice/all
insert into privileges (role_id, resource_id, allow) values ( 2,  167, true); -- apolice/view
insert into privileges (role_id, resource_id, allow) values ( 2,  168, true); -- apolice/add
insert into privileges (role_id, resource_id, allow) values ( 2,  169, true); -- apolice/edit
insert into privileges (role_id, resource_id, allow) values ( 2,  170, true); -- apolice/delete

