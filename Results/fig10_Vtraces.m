% Plot voltage traces from example PC and INs
% Summary diagram for Hippocampus paper
% BPG 23-1-09

FSTEM = 'HAM_P5R1_';   % data file stem

dt = 0.025;

figure;
ms=8;
lw=1;
nr = 5;

STIME = 200;
ETIME = 2050;
VMIN = -90;
VMAX = 50;

subplot(nr,1,1);
FV = [FSTEM 'pvsoma.dat'];   % voltage file
v = load(FV);  % load spike times
t = (0:length(v)-1)*dt;       % extract times
hold on;
plot(t, v, 'k-');   % voltage trace
title('(a) Pattern pyramidal cell');
ylabel('V (mV)');
axis([STIME ETIME VMIN+10 VMAX-30]);

subplot(nr,1,2);
FV = [FSTEM 'AAC.dat'];   % voltage file
v = load(FV);  % load spike times
t = (0:length(v)-1)*dt;       % extract times
hold on;
plot(t, v, 'k-');   % voltage trace
title('(b) Axo-axonic cell');
ylabel('V (mV)');
axis([STIME ETIME VMIN VMAX]);

subplot(nr,1,3);
FV = [FSTEM 'BC.dat'];   % voltage file
v = load(FV);  % load spike times
t = (0:length(v)-1)*dt;       % extract times
hold on;
plot(t, v, 'k-');   % voltage trace
title('(c) Basket cell');
ylabel('V (mV)');
axis([STIME ETIME VMIN VMAX]);

subplot(nr,1,4);
FV = [FSTEM 'BSC.dat'];   % voltage file
v = load(FV);  % load spike times
t = (0:length(v)-1)*dt;       % extract times
hold on;
plot(t, v, 'k-');   % voltage trace
title('(d) Bistratified cell');
ylabel('V (mV)');
axis([STIME ETIME VMIN VMAX]);

subplot(nr,1,5);
FV = [FSTEM 'OLM.dat'];   % voltage file
v = load(FV);  % load spike times
t = (0:length(v)-1)*dt;       % extract times
hold on;
plot(t, v, 'k-');   % voltage trace
title('(e) OLM cell');
ylabel('V (mV)');
xlabel('Time (msecs)');
axis([STIME ETIME VMIN VMAX]);

%print('-dpng', ['Images/' FSTEM 'v']);

    