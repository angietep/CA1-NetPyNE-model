% Plot spikes from list of time vs cell number
% and determine quality of recall
% Summary diagram for Hippocampus paper
% BPG 23-1-09

NCELL = 235;  % number of cells (neurons)
NPCELL = 100; % number of PC (output) cells

NPATT = 1;   % number of patterns
SPATT = 20;   % number of active cells per pattern
CPATT = 1;  % index of cue pattern

RTIME = 50+(250*8);    % run time (msecs)
STIME = 200;
ETIME = 2050;

FPATT = '../Weights/pattsN100S20P5.dat';   % patterns file

FSTEM = 'HAM_P5R1_spt';   % spikes file
FSPIKE = [FSTEM '.dat'];   % spikes file

patts = load(FPATT);   % load stored patterns
cue = patts(:,CPATT);   % extract cue pattern

sp = load(FSPIKE);  % load spike times
st = sp(:,1);       % extract times
cell = sp(:,2);     % extract corresponding cell indices
% extract PC spiking
stp = st(cell < NPCELL);
cellp = cell(cell < NPCELL);

% Analyse spiking over time and compare with cue
DT = 1; % sliding time
%TW = 5;    % width of sliding time window
TW = 10;    % width of sliding time window

ti = 0:DT:RTIME-TW;
NW = length(ti);   % number of time windows
nc = zeros(NW,1);
ha = zeros(NW,1);
co = zeros(NW,1);
an = zeros(NW,1);
mc = mean(cue); % mean cue activity

for i=1:NW
    rp = cellp(stp>=ti(i) & stp<ti(i)+TW); % active cells in sliding window
    nc(i) = length(rp);    % number of active cells in window
    p = zeros(NPCELL,1);
    p(rp+1,1) = 1;  % recalled pattern
    ha(i) = (sum(p == cue)/NPCELL);  % hamming distance
    mp = mean(p);   % mean pattern activity
    % correlation (normalised dot product)
    if mp == 0
        co(i) = 0;
    else
        co(i) = dot(p,cue)/sqrt(sum(p)*sum(cue));
    end;    
    % angle (Graham & Willshaw 97)
    if mp == 0 | mp == 1
        an(i) = 0;
    else
        an(i) = sum((p-mp).*(cue-mc))/sqrt(sum((p-mp).^2)*sum((cue-mc).^2));
    end;
end;

% Generate figure
figure;
ms=8;
lw=2;

subplot(4,1,1);
plot(sp(:,1), sp(:,2), 'k.', 'markersize', ms);   % raster plot of Sep, EC & CA3 spiking
title('(a) Input spikes');
ylabel('Cell no.');
axis([STIME ETIME NPCELL+4 NPCELL+4+130]);
subplot(4,1,2);
plot(sp(:,1), sp(:,2), 'k.', 'markersize', ms);   % raster plot of PC spiking
title('(b) Pyramidal cell spikes');
ylabel('Cell no.');
axis([STIME ETIME 0 NPCELL-1]);

subplot(4,1,3);
hold on;
plot(ti, nc, 'k-', 'LineWidth', lw); % spike counts
title('(c) PC spike count');
ylabel('Spike count');
axis([STIME ETIME 0 NPCELL]);
subplot(4,1,4);
hold on;
plot(ti, co, 'k-', 'LineWidth', lw); % recall quality
title('(d) Recall quality');
ylabel('Quality');
xlabel('Time (msecs)');
axis([STIME ETIME 0 1.02]);

mean(co(co>0))

%print('-dpng', ['Images/' FSTEM]);


    