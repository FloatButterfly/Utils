
ssimValues=zeros(1,10);
CR=zeros(1,10);
qualityFactor=1:1:10;
for i=1:10
    sum_Bytes1=0;
    sum_Bytes2=0;
    sum_ssim=0;
    for j=0:199
        input_name=sprintf('input_%03d_ground truth.jpg',j);
        I=imread(input_name);
        input_dir=dir(input_name);
        sum_Bytes1=input_dir.bytes+sum_Bytes1;
        out_name=sprintf('%03d_compressed_%02d.jpg',j,qualityFactor(i));
        imwrite(I,out_name,'jpg','Mode','lossy','quality',qualityFactor(i));
        output_dir=dir(out_name);
        sum_Bytes2=output_dir.bytes+sum_Bytes2;
        sum_ssim=sum_ssim+ssim(imread(out_name),I);
    end
    ssimValues(i)=sum_ssim/200;
    CR(i)=sum_Bytes2/sum_Bytes1*100;
    fprintf('%d:B2 %d,B1 %d\n',i,sum_Bytes2,sum_Bytes1);
    fprintf('ssimValues:%g\n',ssimValues(i));
    fprintf('CR:%g\n',CR(i));
end

plot(CR,ssimValues,'b-o');
xlabel('Compression Ratio %');
ylabel('SSIM Value');