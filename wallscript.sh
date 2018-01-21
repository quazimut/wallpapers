cd $1
for img in *.png
do
    COLOR_NAME="${img%%-*}"
    case $COLOR_NAME in
        amoled)
            COLOR="#000000"
            ;;
        dark)
            COLOR="#212121"
            ;;
        light)
            COLOR="#ffffff"
            ;;
        *)
    esac
    rem="${img#*-}"
    case ${rem%%-*} in
        s)
            convert $img -background $COLOR -gravity center -extent 1920x1080 ../outs/desktop-small-$COLOR_NAME-1080.png
            convert $img -background $COLOR -gravity center -extent 1080x1920 ../outs/mobile-small-$COLOR_NAME-1080.png
            ;;
        m)
            convert $img -background $COLOR -gravity center -extent 1920x1080 ../outs/desktop-large-$COLOR_NAME-1080.png
            convert $img -background $COLOR -gravity center -extent 1080x1920 ../outs/mobile-large-$COLOR_NAME-1080.png
            convert $img -background $COLOR -gravity center -extent 2560x1440 ../outs/desktop-small-$COLOR_NAME-1440.png
            convert $img -background $COLOR -gravity center -extent 1440x2560 ../outs/mobile-small-$COLOR_NAME-1440.png
            ;;
        l)
            convert $img -background $COLOR -gravity center -extent 2560x1440 ../outs/desktop-large-$COLOR_NAME-1440.png
            convert $img -background $COLOR -gravity center -extent 1440x2560 ../outs/mobile-large-$COLOR_NAME-1440.png
            convert $img -background $COLOR -gravity center -extent 3840x2160 ../outs/desktop-small-$COLOR_NAME-4K.png
            convert $img -background $COLOR -gravity center -extent 2160x3840 ../outs/mobile-small-$COLOR_NAME-4K.png
            ;;
        xl)
            convert $img -background $COLOR -gravity center -extent 3840x2160 ../outs/desktop-large-$COLOR_NAME-4K.png
            convert $img -background $COLOR -gravity center -extent 2160x3840 ../outs/mobile-large-$COLOR_NAME-4K.png
            ;;
        *)
    esac
done
