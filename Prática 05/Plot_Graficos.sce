clc;
close;

fls=loadfls("pratica.fls"); //carrega o arquivo 

figure(1);
plotvar(fls,"input",[1 2]); 

figure(2);
plotvar(fls,"output", 1); 

figure(3);
plotsurf(fls,[1 2],1);
